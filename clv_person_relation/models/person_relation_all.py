# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# pylint: disable=method-required-super

import collections
import logging

from psycopg2.extensions import AsIs

from odoo import _, api, fields, models
from odoo.exceptions import MissingError, ValidationError
from odoo.tools import drop_view_if_exists

_logger = logging.getLogger(__name__)


# Register relations
RELATIONS_SQL = """\
SELECT
    (rel.id * %%(padding)s) + %(key_offset)s AS id,
    'clv.person.relation' AS res_model,
    rel.id AS res_id,
    rel.left_person_id AS this_person_id,
    rel.right_person_id AS other_person_id,
    rel.type_id,
    rel.date_start,
    rel.date_end,
    %(is_inverse)s as is_inverse
    %(extra_additional_columns)s
FROM clv_person_relation rel"""

# Register inverse relations
RELATIONS_SQL_INVERSE = """\
SELECT
    (rel.id * %%(padding)s) + %(key_offset)s AS id,
    'clv.person.relation',
    rel.id,
    rel.right_person_id,
    rel.left_person_id,
    rel.type_id,
    rel.date_start,
    rel.date_end,
    %(is_inverse)s as is_inverse
    %(extra_additional_columns)s
FROM clv_person_relation rel"""


class PersonRelationAll(models.Model):
    """Model to show each relation from two sides."""

    _auto = False
    _log_access = False
    _name = "clv.person.relation.all"
    _description = "All (non-inverse + inverse) relations between persons"
    _order = "this_person_id, type_selection_id, date_end desc, date_start desc"

    res_model = fields.Char(
        string="Resource Model",
        readonly=True,
        required=True,
        help="The database object this relation is based on.",
    )
    res_id = fields.Integer(
        string="Resource ID",
        readonly=True,
        required=True,
        help="The id of the object in the model this relation is based on.",
    )
    this_person_id = fields.Many2one(
        comodel_name="clv.person", string="One Partner", required=True
    )
    other_person_id = fields.Many2one(
        comodel_name="clv.person", string="Other Partner", required=True
    )
    type_id = fields.Many2one(
        comodel_name="clv.person.relation.type",
        string="Underlying Relation Type",
        readonly=True,
        required=True,
    )
    date_start = fields.Date("Starting date")
    date_end = fields.Date("Ending date")
    is_inverse = fields.Boolean(
        string="Is reverse type?",
        readonly=True,
        help="Inverse relations are from right to left person.",
    )
    type_selection_id = fields.Many2one(
        comodel_name="clv.person.relation.type.selection",
        string="Relation Type",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        readonly=True,
        help="Records with date_end in the past are inactive",
    )
    any_person_id = fields.Many2many(
        comodel_name="clv.person",
        string="Partner",
        compute=lambda self: self.update({"any_person_id": None}),
        search="_search_any_person_id",
    )

    def register_specification(self, register, base_name, is_inverse, select_sql):
        _last_key_offset = register["_lastkey"]
        key_name = base_name + (is_inverse and "_inverse" or "")
        assert key_name not in register
        assert "%%(padding)s" in select_sql
        assert "%(key_offset)s" in select_sql
        assert "%(is_inverse)s" in select_sql
        _last_key_offset += 1
        register["_lastkey"] = _last_key_offset
        register[key_name] = dict(
            base_name=base_name,
            is_inverse=is_inverse,
            key_offset=_last_key_offset,
            select_sql=select_sql
            % {
                "key_offset": _last_key_offset,
                "is_inverse": is_inverse,
                "extra_additional_columns": self._get_additional_relation_columns(),
            },
        )

    def get_register(self):
        register = collections.OrderedDict()
        register["_lastkey"] = -1
        self.register_specification(register, "relation", False, RELATIONS_SQL)
        self.register_specification(register, "relation", True, RELATIONS_SQL_INVERSE)
        return register

    def get_select_specification(self, base_name, is_inverse):
        register = self.get_register()
        key_name = base_name + (is_inverse and "_inverse" or "")
        return register[key_name]

    def _get_statement(self):
        """Allow other modules to add to statement."""
        register = self.get_register()
        union_select = " UNION ".join(
            [register[key]["select_sql"] for key in register if key != "_lastkey"]
        )
        return """\
CREATE OR REPLACE VIEW %%(table)s AS
     WITH base_selection AS (%(union_select)s)
 SELECT
     bas.*,
     CASE
         WHEN NOT bas.is_inverse OR typ.is_symmetric
         THEN bas.type_id * 2
         ELSE (bas.type_id * 2) + 1
     END as type_selection_id,
     (bas.date_end IS NULL OR bas.date_end >= current_date) AS active
     %%(additional_view_fields)s
 FROM base_selection bas
 JOIN clv_person_relation_type typ ON (bas.type_id = typ.id)
 %%(additional_tables)s
        """ % {
            "union_select": union_select
        }

    def _get_padding(self):
        """Utility function to define padding in one place."""
        return 100

    def _get_additional_relation_columns(self):
        """Get additionnal columns from clv_person_relation.

        This allows to add fields to the model clv.person.relation
        and display these fields in the clv.person.relation.all list view.

        :return: ', rel.column_a, rel.column_b_id'
        """
        return ""

    def _get_additional_view_fields(self):
        """Allow inherit models to add fields to view.

        If fields are added, the resulting string must have each field
        prepended by a comma, like so:
            return ', typ.allow_self, typ.left_person_category'
        """
        return ""

    def _get_additional_tables(self):
        """Allow inherit models to add tables (JOIN's) to view.

        Example:
            return 'JOIN type_extention ext ON (bas.type_id = ext.id)'
        """
        return ""

    def _auto_init(self):
        cr = self._cr
        drop_view_if_exists(cr, self._table)
        cr.execute(
            self._get_statement(),
            {
                "table": AsIs(self._table),
                "padding": self._get_padding(),
                "additional_view_fields": AsIs(self._get_additional_view_fields()),
                "additional_tables": AsIs(self._get_additional_tables()),
            },
        )
        return super(PersonRelationAll, self)._auto_init()

    @api.model
    def _search_any_person_id(self, operator, value):
        """Search relation with person, no matter on which side."""
        # pylint: disable=no-self-use
        return [
            "|",
            ("this_person_id", operator, value),
            ("other_person_id", operator, value),
        ]

    def name_get(self):
        return {
            this.id: "%s %s %s"
            % (
                this.this_person_id.name,
                this.type_selection_id.display_name,
                this.other_person_id.name,
            )
            for this in self
        }

    @api.onchange("type_selection_id")
    def onchange_type_selection_id(self):
        """Add domain on persons according to category and contact_type."""

        def check_person_domain(person, person_domain, side):
            """Check wether person_domain results in empty selection
            for person, or wrong selection of person already selected.
            """
            warning = {}
            if person:
                test_domain = [("id", "=", person.id)] + person_domain
            else:
                test_domain = person_domain
            person_model = self.env["clv.person"]
            persons_found = person_model.search(test_domain, limit=1)
            if not persons_found:
                warning["title"] = _("Error!")
                if person:
                    warning["message"] = (
                        _("%s person incompatible with relation type.") % side.title()
                    )
                else:
                    warning["message"] = (
                        _("No %s person available for relation type.") % side
                    )
            return warning

        this_person_domain = []
        other_person_domain = []
        if self.type_selection_id.contact_type_this:
            this_person_domain.append(
                ("is_company", "=", self.type_selection_id.contact_type_this == "c")
            )
        if self.type_selection_id.person_category_this:
            this_person_domain.append(
                ("category_id", "in", self.type_selection_id.person_category_this.ids)
            )
        if self.type_selection_id.contact_type_other:
            other_person_domain.append(
                ("is_company", "=", self.type_selection_id.contact_type_other == "c")
            )
        if self.type_selection_id.person_category_other:
            other_person_domain.append(
                ("category_id", "in", self.type_selection_id.person_category_other.ids)
            )
        result = {
            "domain": {
                "this_person_id": this_person_domain,
                "other_person_id": other_person_domain,
            }
        }
        # Check wether domain results in no choice or wrong choice of persons:
        warning = {}
        person_model = self.env["clv.person"]
        if this_person_domain:
            this_person = False
            if bool(self.this_person_id.id):
                this_person = self.this_person_id
            else:
                this_person_id = (
                    "default_this_person_id" in self.env.context
                    and self.env.context["default_this_person_id"]
                    or "active_id" in self.env.context
                    and self.env.context["active_id"]
                    or False
                )
                if this_person_id:
                    this_person = person_model.browse(this_person_id)
            warning = check_person_domain(this_person, this_person_domain, _("this"))
        if not warning and other_person_domain:
            warning = check_person_domain(
                self.other_person_id, other_person_domain, _("other")
            )
        if warning:
            result["warning"] = warning
        return result

    @api.onchange("this_person_id", "other_person_id")
    def onchange_person_id(self):
        """Set domain on type_selection_id based on person(s) selected."""

        def check_type_selection_domain(type_selection_domain):
            """If type_selection_id already selected, check wether it
            is compatible with the computed type_selection_domain. An empty
            selection can practically only occur in a practically empty
            database, and will not lead to problems. Therefore not tested.
            """
            warning = {}
            if not (type_selection_domain and self.type_selection_id):
                return warning
            test_domain = [
                ("id", "=", self.type_selection_id.id)
            ] + type_selection_domain
            type_model = self.env["clv.person.relation.type.selection"]
            types_found = type_model.search(test_domain, limit=1)
            if not types_found:
                warning["title"] = _("Error!")
                warning["message"] = _(
                    "Relation type incompatible with selected person(s)."
                )
            return warning

        type_selection_domain = []
        if self.this_person_id:
            type_selection_domain += [
                "|",
                ("contact_type_this", "=", False),
                ("contact_type_this", "=", self.this_person_id.get_person_type()),
                "|",
                ("person_category_this", "=", False),
                ("person_category_this", "in", self.this_person_id.category_id.ids),
            ]
        if self.other_person_id:
            type_selection_domain += [
                "|",
                ("contact_type_other", "=", False),
                ("contact_type_other", "=", self.other_person_id.get_person_type()),
                "|",
                ("person_category_other", "=", False),
                ("person_category_other", "in", self.other_person_id.category_id.ids),
            ]
        result = {"domain": {"type_selection_id": type_selection_domain}}
        # Check wether domain results in no choice or wrong choice for
        # type_selection_id:
        warning = check_type_selection_domain(type_selection_domain)
        if warning:
            result["warning"] = warning
        return result

    @api.model
    def _correct_vals(self, vals, type_selection):
        """Fill left and right person from this and other person."""
        vals = vals.copy()
        if "type_selection_id" in vals:
            vals["type_id"] = type_selection.type_id.id
        if type_selection.is_inverse:
            if "this_person_id" in vals:
                vals["right_person_id"] = vals["this_person_id"]
            if "other_person_id" in vals:
                vals["left_person_id"] = vals["other_person_id"]
        else:
            if "this_person_id" in vals:
                vals["left_person_id"] = vals["this_person_id"]
            if "other_person_id" in vals:
                vals["right_person_id"] = vals["other_person_id"]
        # Delete values not in underlying table:
        for key in (
            "this_person_id",
            "type_selection_id",
            "other_person_id",
            "is_inverse",
        ):
            if key in vals:
                del vals[key]
        return vals

    def get_base_resource(self):
        """Get base resource from res_model and res_id."""
        self.ensure_one()
        base_model = self.env[self.res_model]
        return base_model.browse([self.res_id])

    def write_resource(self, base_resource, vals):
        """write handled by base resource."""
        self.ensure_one()
        # write for models other then clv.person.relation SHOULD
        # be handled in inherited models:
        relation_model = self.env["clv.person.relation"]
        assert self.res_model == relation_model._name
        base_resource.write(vals)
        base_resource.flush()

    @api.model
    def _get_type_selection_from_vals(self, vals):
        """Get type_selection_id straight from vals or compute from type_id.
        """
        type_selection_id = vals.get("type_selection_id", False)
        if not type_selection_id:
            type_id = vals.get("type_id", False)
            if type_id:
                is_inverse = vals.get("is_inverse")
                type_selection_id = type_id * 2 + (is_inverse and 1 or 0)
        return (
            type_selection_id
            and self.type_selection_id.browse(type_selection_id)
            or False
        )

    def write(self, vals):
        """For model 'clv.person.relation' call write on underlying model."""
        new_type_selection = self._get_type_selection_from_vals(vals)
        for rec in self:
            type_selection = new_type_selection or rec.type_selection_id
            vals = rec._correct_vals(vals, type_selection)
            base_resource = rec.get_base_resource()
            rec.write_resource(base_resource, vals)
        # Invalidate cache to make clv.person.relation.all reflect changes
        # in underlying clv.person.relation:
        self.invalidate_cache(None, self.ids)
        return True

    @api.model
    def _compute_base_name(self, type_selection):
        """This will be overridden for each inherit model."""
        return "relation"

    @api.model
    def _compute_id(self, base_resource, type_selection):
        """Compute id. Allow for enhancements in inherit model."""
        base_name = self._compute_base_name(type_selection)
        key_offset = self.get_select_specification(
            base_name, type_selection.is_inverse
        )["key_offset"]
        return base_resource.id * self._get_padding() + key_offset

    @api.model
    def create_resource(self, vals, type_selection):
        relation_model = self.env["clv.person.relation"]
        return relation_model.create(vals)

    @api.model
    def create(self, vals):
        """Divert non-problematic creates to underlying table.

        Create a clv.person.relation but return the converted id.
        """
        type_selection = self._get_type_selection_from_vals(vals)
        if not type_selection:  # Should not happen
            raise ValidationError(_("No relation type specified in vals: %s.") % vals)
        vals = self._correct_vals(vals, type_selection)
        base_resource = self.create_resource(vals, type_selection)
        res_id = self._compute_id(base_resource, type_selection)
        return self.browse(res_id)

    def unlink_resource(self, base_resource):
        """Delegate unlink to underlying model."""
        self.ensure_one()
        # unlink for models other then clv.person.relation SHOULD
        # be handled in inherited models:
        relation_model = self.env["clv.person.relation"]
        assert self.res_model == relation_model._name
        base_resource.unlink()

    def unlink(self):
        """For model 'clv.person.relation' call unlink on underlying model.
        """
        for rec in self:
            try:
                base_resource = rec.get_base_resource()
            except MissingError:
                continue
            rec.unlink_resource(base_resource)
        return True

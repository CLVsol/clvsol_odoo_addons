# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
For the model defined here _auto is set to False to prevent creating a
database file. The model is based on a SQL view based on
clv_person_relation_type where each type is included in the
result set twice, so it appears that the connection type and the inverse
type are separate records..

The original function _auto_init is still called because this function
normally (if _auto == True) not only creates the db tables, but it also takes
care of registering all fields in ir_model_fields. This is needed to make
the field labels translatable.
"""

from psycopg2.extensions import AsIs

from odoo import api, fields, models
from odoo.tools import drop_view_if_exists


class PersonRelationTypeSelection(models.Model):
    """Virtual relation types"""

    _name = "clv.person.relation.type.selection"
    _description = "All relation types"
    _auto = False  # Do not try to create table in _auto_init(..)
    _foreign_keys = []
    _log_access = False
    _order = "name asc"

    type_id = fields.Many2one(comodel_name="clv.person.relation.type", string="Type")
    name = fields.Char("Name")
    is_inverse = fields.Boolean(
        string="Is reverse type?",
        help="Inverse relations are from right to left person.",
    )
    person_category_this = fields.Many2one(
        comodel_name="clv.person.category", string="Current record's category"
    )
    person_category_other = fields.Many2one(
        comodel_name="clv.person.category", string="Other record's category"
    )
    allow_self = fields.Boolean(string="Reflexive")
    is_symmetric = fields.Boolean(string="Symmetric")

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
            """\
CREATE OR REPLACE VIEW %(table)s AS
     WITH selection_type AS (
 SELECT
     id * 2 AS id,
     id AS type_id,
     name AS name,
     False AS is_inverse,
     person_category_left AS person_category_this,
     person_category_right AS person_category_other
 FROM %(underlying_table)s
 UNION SELECT
     (id * 2) + 1,
     id,
     name_inverse,
     True,
     person_category_right,
     person_category_left
     FROM %(underlying_table)s
     WHERE not is_symmetric
 )
 SELECT
     bas.*,
     typ.allow_self,
     typ.is_symmetric
     %(additional_view_fields)s
 FROM selection_type bas
 JOIN clv_person_relation_type typ ON (bas.type_id = typ.id)
     %(additional_tables)s
            """,
            {
                "table": AsIs(self._table),
                "underlying_table": AsIs("clv_person_relation_type"),
                "additional_view_fields": AsIs(self._get_additional_view_fields()),
                "additional_tables": AsIs(self._get_additional_tables()),
            },
        )
        return super(PersonRelationTypeSelection, self)._auto_init()

    def name_get(self):
        """Get name or name_inverse from underlying model."""
        return [
            (
                this.id,
                this.is_inverse and this.type_id.name_inverse or this.type_id.display_name,
            )
            for this in self
        ]

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """Search for name or inverse name in underlying model."""
        return self.search(
            [
                "|",
                ("type_id.name", operator, name),
                ("type_id.name_inverse", operator, name),
            ] + (args or []),
            limit=limit,
        ).name_get()

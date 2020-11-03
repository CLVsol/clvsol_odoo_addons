# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Support connections between persons."""

import numbers

from odoo import _, api, exceptions, fields, models
from odoo.osv.expression import FALSE_LEAF, OR, is_leaf


class Person(models.Model):
    """Extend person with relations and allow to search for relations
    in various ways.
    """

    # pylint: disable=invalid-name
    # pylint: disable=no-member
    _inherit = "clv.person"

    relation_count = fields.Integer(
        string="Relation Count", compute="_compute_relation_count"
    )
    relation_all_ids = fields.One2many(
        comodel_name="clv.person.relation.all",
        inverse_name="this_person_id",
        string="All relations with current person",
        auto_join=True,
        copy=False,
    )
    search_relation_type_id = fields.Many2one(
        comodel_name="clv.person.relation.type.selection",
        compute=lambda self: self.update({"search_relation_type_id": None}),
        search="_search_relation_type_id",
        string="Has relation of type",
    )
    search_relation_person_id = fields.Many2one(
        comodel_name="clv.person",
        compute=lambda self: self.update({"search_relation_person_id": None}),
        search="_search_related_person_id",
        string="Has relation with",
    )
    search_relation_date = fields.Date(
        compute=lambda self: self.update({"search_relation_date": None}),
        search="_search_relation_date",
        string="Relation valid",
    )
    search_relation_person_category_id = fields.Many2one(
        comodel_name="clv.person.category",
        compute=lambda self: self.update({"search_relation_person_category_id": None}),
        search="_search_related_person_category_id",
        string="Has relation with a person in category",
    )

    @api.depends("relation_all_ids")
    def _compute_relation_count(self):
        """Count the number of relations this person has for Smart Button

        Don't count inactive relations.
        """
        for rec in self:
            rec.relation_count = len(rec.relation_all_ids.filtered("active"))

    @api.model
    def _search_relation_type_id(self, operator, value):
        """Search persons based on their type of relations."""
        result = []
        SUPPORTED_OPERATORS = (
            "=",
            "!=",
            "like",
            "not like",
            "ilike",
            "not ilike",
            "in",
            "not in",
        )
        if operator not in SUPPORTED_OPERATORS:
            raise exceptions.ValidationError(
                _('Unsupported search operator "%s"') % operator
            )
        type_selection_model = self.env["clv.person.relation.type.selection"]
        relation_type_selection = []
        if operator == "=" and isinstance(value, numbers.Integral):
            relation_type_selection += type_selection_model.browse(value)
        elif operator == "!=" and isinstance(value, numbers.Integral):
            relation_type_selection = type_selection_model.search(
                [("id", operator, value)]
            )
        else:
            relation_type_selection = type_selection_model.search(
                [
                    "|",
                    ("type_id.name", operator, value),
                    ("type_id.name_inverse", operator, value),
                ]
            )
        if not relation_type_selection:
            result = [FALSE_LEAF]
        for relation_type in relation_type_selection:
            result = OR(
                [
                    result,
                    [("relation_all_ids.type_selection_id.id", "=", relation_type.id)],
                ]
            )
        return result

    @api.model
    def _search_related_person_id(self, operator, value):
        """Find person based on relation with other person."""
        # pylint: disable=no-self-use
        return [("relation_all_ids.other_person_id", operator, value)]

    @api.model
    def _search_relation_date(self, operator, value):
        """Look only for relations valid at date of search."""
        # pylint: disable=no-self-use
        return [
            "&",
            "|",
            ("relation_all_ids.date_start", "=", False),
            ("relation_all_ids.date_start", "<=", value),
            "|",
            ("relation_all_ids.date_end", "=", False),
            ("relation_all_ids.date_end", ">=", value),
        ]

    @api.model
    def _search_related_person_category_id(self, operator, value):
        """Search for person related to a person with search category."""
        # pylint: disable=no-self-use
        return [("relation_all_ids.other_person_id.category_id", operator, value)]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Inject searching for current relation date if we search for
        relation properties and no explicit date was given.
        """
        # pylint: disable=arguments-differ
        # pylint: disable=no-value-for-parameter
        date_args = []
        for arg in args:
            if (
                is_leaf(arg) and isinstance(arg[0], str) and arg[0].startswith("search_relation")
            ):
                if arg[0] == "search_relation_date":
                    date_args = []
                    break
                if not date_args:
                    date_args = [("search_relation_date", "=", fields.Date.today())]
        # because of auto_join, we have to do the active test by hand
        active_args = []
        if self.env.context.get("active_test", True):
            for arg in args:
                if (
                    is_leaf(arg) and isinstance(arg[0], str) and arg[0].startswith("search_relation")
                ):
                    active_args = [("relation_all_ids.active", "=", True)]
                    break
        return super(Person, self).search(
            args + date_args + active_args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )

    def get_person_type(self):
        """Get person type for relation.
        :return: 'c' for company or 'p' for person
        :rtype: str
        """
        self.ensure_one()
        return "c" if self.is_company else "p"

    def action_view_relations(self):
        for contact in self:
            relation_model = self.env["clv.person.relation.all"]
            relation_ids = relation_model.search(
                [
                    "|",
                    ("this_person_id", "=", contact.id),
                    ("other_person_id", "=", contact.id),
                ]
            )
            action = self.env.ref(
                "clv_person_relation.clv_person_relation_action"
            ).read()[0]
            action["domain"] = [("id", "in", relation_ids.ids)]
            context = action.get("context", "{}").strip()[1:-1]
            elements = context.split(",") if context else []
            to_add = [
                """'search_default_this_person_id': {0},
                        'default_this_person_id': {0},
                        'active_model': 'clv.person',
                        'active_id': {0},
                        'active_ids': [{0}],
                        'active_test': False""".format(
                    contact.id
                )
            ]
            context = "{" + ", ".join(elements + to_add) + "}"
            action["context"] = context
            return action

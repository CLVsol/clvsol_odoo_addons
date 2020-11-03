# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Store relations (connections) between persons."""

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PersonRelation(models.Model):
    """Model clv.person.relation is used to describe all links or relations
    between persons in the database.

    This model is actually only used to store the data. The model
    clv.person.relation.all, based on a view that contains each record
    two times, once for the normal relation, once for the inverse relation,
    will be used to maintain the data.
    """

    _name = "clv.person.relation"
    _description = "Person relation"

    left_person_id = fields.Many2one(
        comodel_name="clv.person",
        string="Source Person",
        required=True,
        auto_join=True,
        ondelete="cascade",
    )
    right_person_id = fields.Many2one(
        comodel_name="clv.person",
        string="Destination Person",
        required=True,
        auto_join=True,
        ondelete="cascade",
    )
    type_id = fields.Many2one(
        comodel_name="clv.person.relation.type",
        string="Type",
        required=True,
        auto_join=True,
    )
    date_start = fields.Date("Starting date")
    date_end = fields.Date("Ending date")

    @api.model
    def create(self, vals):
        """Override create to correct values, before being stored."""
        context = self.env.context
        if "left_person_id" not in vals and context.get("active_id"):
            vals["left_person_id"] = context.get("active_id")
        return super(PersonRelation, self).create(vals)

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        """End date should not be before start date, if not filled

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            if (
                record.date_start and record.date_end and record.date_start > record.date_end
            ):
                raise ValidationError(
                    _("The starting date cannot be after the ending date.")
                )

    @api.constrains("left_person_id", "type_id")
    def _check_person_left(self):
        """Check left person for required company or person

        :raises ValidationError: When constraint is violated
        """
        self._check_person("left")

    @api.constrains("right_person_id", "type_id")
    def _check_person_right(self):
        """Check right person for required company or person

        :raises ValidationError: When constraint is violated
        """
        self._check_person("right")

    def _check_person(self, side):
        """Check person for required company or person, and for category

        :param str side: left or right
        :raises ValidationError: When constraint is violated
        """
        for record in self:
            assert side in ["left", "right"]
            person = getattr(record, "%s_person_id" % side)
            category = getattr(record.type_id, "person_category_%s" % side)
            if category and category.id not in person.category_id.ids:
                raise ValidationError(
                    _("The %s person does not have category %s.")
                    % (side, category.name)
                )

    @api.constrains("left_person_id", "right_person_id")
    def _check_not_with_self(self):
        """Not allowed to link person to same person

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            if record.left_person_id == record.right_person_id:
                if not (record.type_id and record.type_id.allow_self):
                    raise ValidationError(
                        _("Persons cannot have a relation with themselves.")
                    )

    @api.constrains(
        "left_person_id", "type_id", "right_person_id", "date_start", "date_end"
    )
    def _check_relation_uniqueness(self):
        """Forbid multiple active relations of the same type between the same
        persons

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            domain = [
                ("type_id", "=", record.type_id.id),
                ("id", "!=", record.id),
                ("left_person_id", "=", record.left_person_id.id),
                ("right_person_id", "=", record.right_person_id.id),
            ]
            if record.date_start:
                domain += [
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">=", record.date_start),
                ]
            if record.date_end:
                domain += [
                    "|",
                    ("date_start", "=", False),
                    ("date_start", "<=", record.date_end),
                ]
            if record.search(domain):
                raise ValidationError(
                    _("There is already a similar relation with " "overlapping dates")
                )

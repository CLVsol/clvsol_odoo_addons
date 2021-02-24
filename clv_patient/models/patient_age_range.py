# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PatientAgeRange(models.Model):
    _name = "clv.patient.age_range"
    _description = "Patient Age Range"

    def _default_age_from(self):
        age_from = 0
        last_age_range = self.env["clv.patient.age_range"].search(
            [], order="age_to desc", limit=1
        )
        if last_age_range:
            age_from = last_age_range.age_to + 1
        return age_from

    name = fields.Char(string="Name", required=True)
    age_from = fields.Integer(
        string="From", required=True, default=lambda self: self._default_age_from()
    )
    age_to = fields.Integer(string="To", required=True)

    _sql_constraints = [("name_uniq", "unique (name)", "A name must be unique !")]

    @api.constrains("age_from", "age_to")
    def _validate_range(self):
        for rec in self:
            if rec.age_from >= rec.age_to:
                raise ValidationError(
                    _("%s is not a valid range (%s >= %s)")
                    % (rec.name, rec.age_from, rec.age_to)
                )
            range_id = rec.search(
                [
                    ("age_from", "<=", rec.age_to),
                    ("age_to", ">=", rec.age_from),
                    ("id", "!=", rec.id),
                ],
                limit=1,
            )
            if range_id:
                raise ValidationError(
                    _("%s is overalapping with range %s") % (rec.name, range_id.name)
                )


class Patient(models.Model):
    _inherit = "clv.patient"

    age_range_id = fields.Many2one(
        "clv.patient.age_range",
        "Age Range",
        compute="_compute_age_range_id",
        store=True,
    )

    @api.depends("age_reference_years")
    def _compute_age_range_id(self):
        age_ranges = self.env["clv.patient.age_range"].search([])
        for record in self:
            if not record.age_reference_years:
                age_range = False
            else:
                y_pos = record.age_reference_years.find('y')
                if y_pos > 0:
                    age_reference = int(record.age_reference_years[0:y_pos])
                age_range = (
                    age_ranges.filtered(
                        lambda age_range: age_range.age_from <= age_reference <= age_range.age_to
                    ) or False
                )
            if record.is_deceased is not True:
                if record.age_range_id != age_range:
                    record.age_range_id = age_range and age_range.id or age_range
            else:
                record.age_range_id = False

    @api.model
    def _patient_update_age_range_id_cron(self):
        """
        This method is called from a cron job.
        It is used to update age range on contact
        """
        patients = self.search([("birthday", "!=", False)])
        patients._compute_age_range_id()

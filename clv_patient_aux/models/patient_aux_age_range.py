# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PatientAux(models.Model):
    _inherit = "clv.patient_aux"

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
    def _patient_aux_update_age_range_id_cron(self):
        """
        This method is called from a cron job.
        It is used to update age range on contact
        """
        patients_aux = self.search([("birthday", "!=", False)])
        patients_aux._compute_age_range_id()

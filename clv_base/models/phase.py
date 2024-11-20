# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    patient_ids = fields.One2many(
        comodel_name='clv.patient',
        inverse_name='phase_id',
        string='Patients',
        readonly=True
    )
    count_patients = fields.Integer(
        string='Patients (count)',
        compute='_compute_patient_ids_and_count',
    )

    def _compute_patient_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            patients = self.env['clv.patient'].search(search_domain)

            record.count_patients = len(patients)
            record.patient_ids = [(6, 0, patients.ids)]


class Patient(models.Model):
    _inherit = 'clv.patient'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )

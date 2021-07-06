# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    patient_history_ids = fields.One2many(
        comodel_name='clv.patient.history',
        inverse_name='phase_id',
        string='Patients (History)',
        readonly=True
    )
    count_patient_histories = fields.Integer(
        string='Patients (History) (count)',
        compute='_compute_patient_history_ids_and_count',
    )

    def _compute_patient_history_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            patient_histories = self.env['clv.patient.history'].search(search_domain)

            record.count_patient_histories = len(patient_histories)
            record.patient_history_ids = [(6, 0, patient_histories.ids)]


class PatientHistory(models.Model):
    _inherit = 'clv.patient.history'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PatientHistory(models.Model):
    _inherit = 'clv.patient.history'

    patient_id = fields.Many2one(
        comodel_name='clv.patient',
        string='Patient',
        ondelete='restrict'
    )

    responsible_id = fields.Many2one(
        comodel_name='clv.patient',
        string='Responsible',
        ondelete='restrict'
    )
    caregiver_id = fields.Many2one(
        comodel_name='clv.patient',
        string='Caregiver',
        ondelete='restrict'
    )


class Patient(models.Model):
    _inherit = 'clv.patient'

    patient_history_ids = fields.One2many(
        comodel_name='clv.patient.history',
        inverse_name='patient_id',
        string='Patients (History)'
    )
    count_patient_histories = fields.Integer(
        string='Patients (History) (count)',
        compute='_compute_count_patient_histories',
    )

    @api.depends('patient_history_ids')
    def _compute_count_patient_histories(self):
        for r in self:
            r.count_patient_histories = len(r.patient_history_ids)

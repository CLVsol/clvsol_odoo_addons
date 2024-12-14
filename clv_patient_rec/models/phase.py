# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    patient_rec_ids = fields.One2many(
        comodel_name='clv.patient_rec',
        inverse_name='phase_id',
        string='Patients (Rec)',
        readonly=True
    )
    count_patients_rec = fields.Integer(
        string='Patients (Rec) (count)',
        compute='_compute_patient_rec_ids_and_count',
    )

    def _compute_patient_rec_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            patients_rec = self.env['clv.patient_rec'].search(search_domain)

            record.count_patients_rec = len(patients_rec)
            record.patient_rec_ids = [(6, 0, patients_rec.ids)]


class PatientRec(models.Model):
    _inherit = 'clv.patient_rec'

    def _default_phase_id(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip()
        phase_id = False
        if param_value:
            phase_id = int(param_value)
        return phase_id
    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        default=_default_phase_id,
        ondelete='restrict'
    )

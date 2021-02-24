# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    patient_aux_ids = fields.One2many(
        comodel_name='clv.patient_aux',
        inverse_name='phase_id',
        string='Patients (Aux)',
        readonly=True
    )
    count_patients_aux = fields.Integer(
        string='Patients (Aux) (count)',
        compute='_compute_patient_aux_ids_and_count',
    )

    def _compute_patient_aux_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            patients_aux = self.env['clv.patient_aux'].search(search_domain)

            record.count_patients_aux = len(patients_aux)
            record.patient_aux_ids = [(6, 0, patients_aux.ids)]


class PatientAux(models.Model):
    _inherit = 'clv.patient_aux'

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

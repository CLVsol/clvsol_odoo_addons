# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class PatientAux(models.Model):
    _inherit = 'clv.patient_aux'

    reg_state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
         ('verified', 'Verified'),
         ('ready', 'Ready'),
         ('done', 'Done'),
         ('canceled', 'Canceled')
         ], string='Register State', default='draft', readonly=True, required=True
    )

    @api.model
    def is_allowed_transition_reg_state(self, old_reg_state, new_reg_state):
        # allowed = [
        #     ('canceled', 'draft'),
        # ]
        # return (old_reg_state, new_reg_state) in allowed
        return True

    def change_reg_state(self, new_reg_state):
        for patient_aux in self:
            if patient_aux.is_allowed_transition_reg_state(patient_aux.reg_state, new_reg_state):
                patient_aux.reg_state = new_reg_state
            else:
                raise UserError(
                    'Status transition (' + patient_aux.reg_state + ', ' + new_reg_state + ') is not allowed!')

    def action_draft(self):
        for patient_aux in self:
            patient_aux.change_reg_state('draft')

    def action_revised(self):
        for patient_aux in self:
            patient_aux.change_reg_state('revised')

    def action_verified(self):
        for patient_aux in self:
            patient_aux.change_reg_state('verified')

    def action_ready(self):
        for patient_aux in self:
            patient_aux.change_reg_state('ready')

    def action_done(self):
        for patient_aux in self:
            patient_aux.change_reg_state('done')

    def action_cancel(self):
        for patient_aux in self:
            patient_aux.change_reg_state('canceled')

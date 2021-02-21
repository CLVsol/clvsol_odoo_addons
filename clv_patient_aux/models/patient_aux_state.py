# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class PatientAux(models.Model):
    _inherit = 'clv.patient_aux'

    state = fields.Selection(
        [('new', 'New'),
         ('available', 'Available'),
         ('waiting', 'Waiting'),
         ('selected', 'Selected'),
         ('unselected', 'Unselected'),
         ('unavailable', 'Unavailable'),
         ('unknown', 'Unknown')
         ], string='Patient State', default='new', readonly=True, required=True
    )

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        # allowed = [
        #     ('unavailable', 'new'),
        # ]
        # return (old_state, new_state) in allowed
        return True

    def change_state(self, new_state):
        for patient_aux in self:
            if patient_aux.is_allowed_transition(patient_aux.state, new_state):
                patient_aux.state = new_state
            else:
                raise UserError('Status transition (' + patient_aux.state + ', ' + new_state + ') is not allowed!')

    def action_new(self):
        for patient_aux in self:
            patient_aux.change_state('new')

    def action_available(self):
        for patient_aux in self:
            patient_aux.change_state('available')

    def action_waiting(self):
        for patient_aux in self:
            patient_aux.change_state('waiting')

    def action_select(self):
        for patient_aux in self:
            patient_aux.change_state('selected')

    def action_unselect(self):
        for patient_aux in self:
            patient_aux.change_state('unselected')

    def action_unavailable(self):
        for patient_aux in self:
            patient_aux.change_state('unavailable')

    def action_unknown(self):
        for patient_aux in self:
            patient_aux.change_state('unknown')

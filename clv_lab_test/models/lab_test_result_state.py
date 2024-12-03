# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class LabTestResult(models.Model):
    _inherit = 'clv.lab_test.result'

    state = fields.Selection(
        [('new', 'New'),
         ('received', 'Received'),
         ('available', 'Available'),
         ('approved', 'Approved'),
         ('discarded', 'Discarded')
         ], string='Result State', default='new', readonly=True, required=True
    )

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        # allowed = [
        #     ('discarded', 'new'),
        # ]
        # return (old_state, new_state) in allowed
        return True

    def change_state(self, new_state):
        for lab_test_result in self:
            if lab_test_result.is_allowed_transition(lab_test_result.state, new_state):
                lab_test_result.state = new_state
            else:
                raise UserError('Status transition (' + lab_test_result.state + ', ' + new_state + ') is not allowed!')

    def action_new(self):
        for lab_test_result in self:
            lab_test_result.change_state('new')

    def action_available(self):
        for lab_test_result in self:
            lab_test_result.change_state('available')

    def action_approve(self):
        for lab_test_result in self:
            lab_test_result.change_state('approved')

    def action_discard(self):
        for lab_test_result in self:
            lab_test_result.change_state('discarded')

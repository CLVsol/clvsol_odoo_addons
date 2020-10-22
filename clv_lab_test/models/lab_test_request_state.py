# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class LabTestRequest(models.Model):
    _inherit = 'clv.lab_test.request'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('received', 'Received'),
         ('cancelled', 'Cancelled'),
         ], 'Request State', default='draft', readonly=True
    )

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        # allowed = [
        #     ('draft', 'received'),
        # ]
        # return (old_state, new_state) in allowed
        return True

    def change_state(self, new_state):
        for lab_test_request in self:
            if lab_test_request.is_allowed_transition(lab_test_request.state, new_state):
                lab_test_request.state = new_state
            else:
                raise UserError(
                    'Status transition (' + lab_test_request.state + ', ' + new_state + ') is not allowed!')

    def action_draft(self):
        for lab_test_request in self:
            lab_test_request.change_state('draft')

    def action_received(self):
        for lab_test_request in self:
            lab_test_request.change_state('received')

    def action_cancel(self):
        for lab_test_request in self:
            lab_test_request.change_state('cancelled')

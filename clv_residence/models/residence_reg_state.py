# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class Residence(models.Model):
    _inherit = 'clv.residence'

    reg_state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
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
        for residence in self:
            if residence.is_allowed_transition_reg_state(residence.reg_state, new_reg_state):
                residence.reg_state = new_reg_state
            else:
                raise UserError('Status transition (' + residence.reg_state + ', ' + new_reg_state + ') is not allowed!')

    def action_draft(self):
        for residence in self:
            residence.change_reg_state('draft')

    def action_revised(self):
        for residence in self:
            residence.change_reg_state('revised')

    def action_done(self):
        for residence in self:
            residence.change_reg_state('done')

    def action_cancel(self):
        for residence in self:
            residence.change_reg_state('canceled')

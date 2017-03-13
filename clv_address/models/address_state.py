# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import api, fields, models
from openerp.exceptions import UserError


class Address(models.Model):
    _inherit = 'clv.address'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
         ('waiting', 'Waiting'),
         ('selected', 'Selected'),
         ('unselected', 'Unselected'),
         ('canceled', 'Canceled')
         ], string='Status', default='draft', readonly=True, required=True
    )

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        # allowed = [
        #     ('canceled', 'draft'),
        #     ('draft', 'revised'),
        #     ('waiting', 'revised'),
        #     ('selected', 'revised'),
        #     ('unselected', 'revised'),
        #     ('revised', 'waiting'),
        #     ('revised', 'selected'),
        #     ('waiting', 'selected'),
        #     ('unselected', 'selected'),
        #     ('revised', 'unselected'),
        #     ('waiting', 'unselected'),
        #     ('selected', 'unselected'),
        #     ('draft', 'canceled'),
        #     ('revised', 'canceled')
        # ]
        # return (old_state, new_state) in allowed
        return True

    @api.multi
    def change_state(self, new_state):
        for address in self:
            if address.is_allowed_transition(address.state, new_state):
                address.state = new_state
            else:
                raise UserError('Status transition (' + address.state + ', ' + new_state + ') is not allowed!')

    @api.multi
    def action_draft(self):
        for address in self:
            address.change_state('draft')

    @api.multi
    def action_revised(self):
        for address in self:
            address.change_state('revised')

    @api.multi
    def action_waiting(self):
        for address in self:
            address.change_state('waiting')

    @api.multi
    def action_select(self):
        for address in self:
            address.change_state('selected')

    @api.multi
    def action_unselect(self):
        for address in self:
            address.change_state('unselected')

    @api.multi
    def action_cancel(self):
        for address in self:
            address.change_state('canceled')

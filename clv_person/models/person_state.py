# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class Person(models.Model):
    _inherit = 'clv.person'

    state = fields.Selection(
        [('new', 'New'),
         ('available', 'Available'),
         ('waiting', 'Waiting'),
         ('selected', 'Selected'),
         ('unselected', 'Unselected'),
         ('unavailable', 'Unavailable'),
         ('unknown', 'Unknown')
         ], string='Person State', default='new', readonly=True, required=True
    )

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        # allowed = [
        #     ('unavailable', 'new'),
        # ]
        # return (old_state, new_state) in allowed
        return True

    def change_state(self, new_state):
        for person in self:
            if person.is_allowed_transition(person.state, new_state):
                person.state = new_state
            else:
                raise UserError('Status transition (' + person.state + ', ' + new_state + ') is not allowed!')

    def action_new(self):
        for person in self:
            person.change_state('new')

    def action_available(self):
        for person in self:
            person.change_state('available')

    def action_waiting(self):
        for person in self:
            person.change_state('waiting')

    def action_select(self):
        for person in self:
            person.change_state('selected')

    def action_unselect(self):
        for person in self:
            person.change_state('unselected')

    def action_unavailable(self):
        for person in self:
            person.change_state('unavailable')

    def action_unknown(self):
        for person in self:
            person.change_state('unknown')

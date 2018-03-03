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

from odoo import api, fields, models


class CardLog(models.Model):
    _description = 'Card Log'
    _name = 'clv.card.log'
    _inherit = 'clv.object.log'

    card_id = fields.Many2one(
        comodel_name='clv.card',
        string='Card',
        required=True,
        ondelete='cascade'
    )


class Card(models.Model):
    _name = "clv.card"
    _inherit = 'clv.card', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.card.log',
        inverse_name='card_id',
        string='Card Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, card_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'card_id': card_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.env['clv.card.log'].create(vals)

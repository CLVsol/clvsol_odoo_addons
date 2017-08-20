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


class AddressHistoryLog(models.Model):
    _description = 'Address History Log'
    _name = 'clv.address.history.log'
    _inherit = 'clv.object.log'

    address_history_id = fields.Many2one(
        comodel_name='clv.address.history',
        string='Address History',
        required=True,
        ondelete='cascade'
    )


class AddressHistory(models.Model):
    _name = "clv.address.history"
    _inherit = 'clv.address.history', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.address.history.log',
        inverse_name='address_history_id',
        string='Address History Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, address_history_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            if str(values).find("'category_ids': clv.address.history.category(") == -1:
                vals = {
                    'address_history_id': address_history_id,
                    'values': values,
                    'action': action,
                    'notes': notes,
                }
                self.env['clv.address.history.log'].create(vals)

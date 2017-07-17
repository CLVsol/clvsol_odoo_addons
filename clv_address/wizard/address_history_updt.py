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

import logging

from odoo import api, fields, models
from odoo import exceptions

_logger = logging.getLogger(__name__)


class AddressHistoryUpdate(models.TransientModel):
    _name = 'clv.address.history_updt'

    def _default_address_ids(self):
        return self._context.get('active_ids')
    address_ids = fields.Many2many(
        comodel_name='clv.address',
        relation='clv_address_history_updt_rel',
        string='Addresses',
        default=_default_address_ids
    )
    sign_in_date = fields.Date(
        string='Sign in date',
        required=False,
    )
    sign_out_date = fields.Date(
        string="Sign out date",
        required=False
    )

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_address_history_updt(self):
        self.ensure_one()

        AddressHistory = self.env['clv.address.history']

        for address in self.address_ids:

            if self.sign_out_date is False:
                raise exceptions.ValidationError('The "Sign out date" has not been defined!')
                return self._reopen_form()

            if self.sign_in_date is False:
                raise exceptions.ValidationError('The "Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s', '>>>>>', address.name)

            if address.global_marker_id.id is not False:

                address_history = AddressHistory.search([
                    ('address_id', '=', address.id),
                    ('global_marker_id', '=', address.global_marker_id.id),
                    ('sign_out_date', '=', False),
                ])

                if address_history.id is False:

                    address_history_2 = AddressHistory.search([
                        ('address_id', '=', address.id),
                        ('sign_out_date', '=', False),
                    ])
                    if address_history_2.id is not False:
                        address_history_2.sign_out_date = self.sign_out_date
                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', address_history_2.global_marker_id.name,
                                                     address_history_2.sign_in_date,
                                                     address_history_2.sign_out_date)

                    values = {
                        'address_id': address.id,
                        'sign_in_date': self.sign_in_date,
                        'global_marker_id': address.global_marker_id.id,
                    }
                    address_history = AddressHistory.create(values)
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', address_history.global_marker_id.name,
                                                 address_history.sign_in_date,
                                                 address_history.sign_out_date)

                else:
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', address_history.global_marker_id.name,
                                                 address_history.sign_in_date,
                                                 address_history.sign_out_date)

            else:

                address_history = AddressHistory.search([
                    ('address_id', '=', address.id),
                    ('sign_out_date', '=', False),
                ])

                if address_history.id is not False:
                    address_history.sign_out_date = self.sign_out_date
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', address_history.global_marker_id.name,
                                                 address_history.sign_in_date,
                                                 address_history.sign_out_date)

        return True
        # return self._reopen_form()

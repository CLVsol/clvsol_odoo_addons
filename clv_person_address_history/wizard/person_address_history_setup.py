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


class PersonAddressHistorySetUp(models.TransientModel):
    _name = 'clv.person.address.history_setup'

    def _default_person_ids(self):
        return self._context.get('active_ids')
    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_address_history_setup_rel',
        string='Persons',
        default=_default_person_ids
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
    def do_person_address_history_setup(self):
        self.ensure_one()

        PersonAddressHistory = self.env['clv.person.address.history']

        for person in self.person_ids:

            if self.sign_out_date is False:
                raise exceptions.ValidationError('The "Sign out date" has not been defined!')
                return self._reopen_form()

            if self.sign_in_date is False:
                raise exceptions.ValidationError('The "Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s %s', '>>>>>', person.name, person.address_id)

            if person.address_id.id is not False and person.global_marker_id.id is not False:

                person_address_history = PersonAddressHistory.search([
                    ('person_id', '=', person.id),
                    ('address_id', '=', person.address_id.id),
                    ('global_marker_id', '=', person.global_marker_id.id),
                    ('sign_out_date', '=', False),
                ])

                if person_address_history.id is False:

                    person_address_history_2 = PersonAddressHistory.search([
                        ('person_id', '=', person.id),
                        ('sign_out_date', '=', False),
                    ])
                    for person_address_history_3 in person_address_history_2:
                        person_address_history_3.sign_out_date = self.sign_out_date
                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', person_address_history_3.address_id.name,
                                                     person_address_history_3.sign_in_date,
                                                     person_address_history_3.sign_out_date)

                    values = {
                        'person_id': person.id,
                        'address_id': person.address_id.id,
                        'role_id': person.person_address_role_id.id,
                        'sign_in_date': self.sign_in_date,
                        'global_marker_id': person.global_marker_id.id,
                    }
                    person_address_history = PersonAddressHistory.create(values)
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', person_address_history.address_id.name,
                                                 person_address_history.sign_in_date,
                                                 person_address_history.sign_out_date)

                else:
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', person_address_history.address_id.name,
                                                 person_address_history.sign_in_date,
                                                 person_address_history.sign_out_date)

            else:

                person_address_history = PersonAddressHistory.search([
                    ('person_id', '=', person.id),
                    ('sign_out_date', '=', False),
                ])

                for person_address_history_4 in person_address_history:
                    person_address_history_4.sign_out_date = self.sign_out_date
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', person_address_history_4.address_id.name,
                                                 person_address_history_4.sign_in_date,
                                                 person_address_history_4.sign_out_date)

        return True
        # return self._reopen_form()

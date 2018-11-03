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


class PersonMngAddressCreate(models.TransientModel):
    _name = 'clv.person.mng.address_create'

    def _default_person_mng_ids(self):
        return self._context.get('active_ids')
    person_mng_ids = fields.Many2many(
        comodel_name='clv.person.mng',
        relation='clv_person_mng_address_create_rel',
        string='Persons (Mng)',
        default=_default_person_mng_ids
    )

    def _default_history_marker_id(self):
        history_marker_id = int(self.env['ir.config_parameter'].get_param(
            'clv.config.settings.current_history_marker_id', '').strip())
        return history_marker_id
    history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='History Marker',
        ondelete='restrict',
        default=_default_history_marker_id
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
    def do_person_mng_address_create(self):
        self.ensure_one()

        if self.history_marker_id.id is False:
            raise exceptions.ValidationError('The "History Marker" has not been defined!')
            return self._reopen_form()

        Address = self.env['clv.address']

        for person_mng in self.person_mng_ids:

            _logger.info(u'>>>>> %s', person_mng.name)

            if person_mng.action_address == 'create':

                address = Address.search([
                    ('street', '=', person_mng.street),
                    ('street2', '=', person_mng.street2),
                ])
                if address.id is False:

                    if person_mng.address_id.id is False:

                        suggested_name = False
                        if person_mng.street:
                            suggested_name = person_mng.street
                            if person_mng.street2:
                                suggested_name = suggested_name + ' - ' + person_mng.street2

                        if suggested_name is not False:

                            state_id = False
                            if person_mng.state_id is not False:
                                state_id = person_mng.state_id.id

                            country_id = False
                            if person_mng.country_id is not False:
                                country_id = person_mng.country_id.id

                            new_category_ids = False
                            if person_mng.addr_category_ids is not False:

                                new_category_ids = []
                                for category_id in person_mng.addr_category_ids:

                                    new_category_ids.append((4, category_id.id))

                            values = {
                                'name': suggested_name,
                                'street': person_mng.street,
                                'street2': person_mng.street2,
                                'zip': person_mng.zip,
                                'city': person_mng.city,
                                'state_id': state_id,
                                'country_id': country_id,
                                'phone': person_mng.phone,
                                'mobile': person_mng.mobile,
                                'category_ids': new_category_ids,
                                'history_marker_id': self.history_marker_id.id,
                            }
                            _logger.info(u'>>>>> %s', values)
                            new_address = Address.create(values)
                            new_address.code = '/'

                            person_mng.address_id = new_address.id

                            _logger.info(u'>>>>>>>>>> %s: %s', 'action_address', person_mng.action_address)

                            person_mng.action_address = 'none'

        return True

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


class PersonOffPersonCreate(models.TransientModel):
    _name = 'clv.person.off.person_create'

    def _default_person_off_ids(self):
        return self._context.get('active_ids')
    person_off_ids = fields.Many2many(
        comodel_name='clv.person.off',
        relation='clv_person_off_person_create_rel',
        string='Persons (Off)',
        default=_default_person_off_ids
    )

    history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='History Marker',
        ondelete='restrict'
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
    def do_person_off_person_create(self):
        self.ensure_one()

        if self.history_marker_id.id is False:
            raise exceptions.ValidationError('The "History Marker" has not been defined!')
            return self._reopen_form()

        Person = self.env['clv.person']

        for person_off in self.person_off_ids:

            _logger.info(u'>>>>> %s', person_off.name)

            if person_off.action_person == 'create':

                if person_off.person_id.id is False:

                    _logger.info(u'>>>>>>>>>> %s: %s', 'action_person', person_off.action_person)

                    responsible_id = False
                    if person_off.responsible_id is not False:
                        responsible_id = person_off.responsible_id.id

                    caregiver_id = False
                    if person_off.caregiver_id is not False:
                        caregiver_id = person_off.caregiver_id.id

                    address_id = False
                    if person_off.address_id is not False:
                        address_id = person_off.address_id.id

                    values = {
                        'name': person_off.name,
                        'gender': person_off.gender,
                        'estimated_age': person_off.estimated_age,
                        'birthday': person_off.birthday,
                        'responsible_id': responsible_id,
                        'caregiver_id': caregiver_id,
                        'address_id': address_id,
                        'phone': person_off.phone,
                        'mobile': person_off.mobile,
                        'history_marker_id': self.history_marker_id.id,
                    }
                    _logger.info(u'>>>>> %s', values)
                    new_person = Person.create(values)
                    new_person.code = '/'

                    person_off.person_id = new_person.id

        return True

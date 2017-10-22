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


class PersonMngPersonAddressMove(models.TransientModel):
    _name = 'clv.person.mng.person_address_move'

    def _default_person_mng_ids(self):
        return self._context.get('active_ids')
    person_mng_ids = fields.Many2many(
        comodel_name='clv.person.mng',
        relation='clv_person_mng_person_address_move_rel',
        string='Persons (Mng)',
        readonly=True,
        default=_default_person_mng_ids
    )

    def _default_origin_addr_id(self):
        person_mng_id = self._context.get('active_id')
        PersonMng = self.env['clv.person.mng']
        person_mng = PersonMng.search([('id', '=', person_mng_id)])
        return person_mng.person_id.address_id.id
    origin_addr_id = fields.Many2one(
        comodel_name='clv.address',
        string='Origin Address',
        ondelete='restrict',
        readonly=True,
        default=_default_origin_addr_id
    )

    def _default_origin_addr_person_ids(self):
        person_mng_id = self._context.get('active_id')
        PersonMng = self.env['clv.person.mng']
        person_mng = PersonMng.search([('id', '=', person_mng_id)])
        Person = self.env['clv.person']
        address_id = person_mng.person_id.address_id.id
        persons = False
        if address_id is not False:
            persons = Person.search([('address_id', '=', address_id)])
        return persons
    origin_addr_person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_mng_person_address_move_origin_addr_rel',
        string='Persons (Origin Address)',
        readonly=True,
        default=_default_origin_addr_person_ids
    )

    def _default_destination_addr_id(self):
        person_mng_id = self._context.get('active_id')
        PersonMng = self.env['clv.person.mng']
        person_mng = PersonMng.search([('id', '=', person_mng_id)])
        return person_mng.address_id.id
    destination_addr_id = fields.Many2one(
        comodel_name='clv.address',
        string='Destination Address',
        ondelete='restrict',
        readonly=True,
        default=_default_destination_addr_id
    )

    def _default_destination_addr_person_ids(self):
        person_mng_id = self._context.get('active_id')
        PersonMng = self.env['clv.person.mng']
        person_mng = PersonMng.search([('id', '=', person_mng_id)])
        Person = self.env['clv.person']
        address_id = person_mng.address_id.id
        persons = False
        if address_id is not False:
            persons = Person.search([('address_id', '=', address_id)])
        return persons
    destination_addr_person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_mng_person_address_move_destination_addr_rel',
        string='Persons (Destination Address)',
        readonly=True,
        default=_default_destination_addr_person_ids
    )

    person_category_ids = fields.Many2many(
        comodel_name='clv.person.category',
        relation='clv_person_mng_person_address_move_person_category_rel',
        column1='person_id',
        column2='category_id',
        string='Person Categories'
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
    def do_person_mng_person_address_move(self):
        self.ensure_one()

        if self.person_category_ids.id == []:
            raise exceptions.ValidationError('The "Person Catgegories" has not been defined!')
            return self._reopen_form()

        for person_mng in self.person_mng_ids:

            if (person_mng.action_person_address == 'move') and \
               (person_mng.action_person == 'none') and \
               (person_mng.action_address == 'none'):

                _logger.info(u'>>>>> %s', person_mng.name)

                if self.destination_addr_id:
                    person_mng.person_id.address_id = self.destination_addr_id

                    m2m_list = []
                    for person_category_id in self.person_category_ids:
                        m2m_list.append((4, person_category_id.id))
                    _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                    person_mng.person_id.category_ids = m2m_list

                    _logger.info(u'>>>>>>>>>> %s', person_mng.person_id.address_id.name)

                    person_mng.action_person_address = 'none'

                    Person = self.env['clv.person']

                    address_id = self.origin_addr_id.id
                    persons = False
                    if address_id is not False:
                        persons = Person.search([('address_id', '=', address_id)])
                    _logger.info(u'>>>>>>>>>> %s', self.origin_addr_person_ids)
                    self.origin_addr_person_ids = persons
                    _logger.info(u'>>>>>>>>>> %s', self.origin_addr_person_ids)

                    address_id = person_mng.address_id.id
                    persons = False
                    if address_id is not False:
                        persons = Person.search([('address_id', '=', address_id)])
                    _logger.info(u'>>>>>>>>>> %s', self.destination_addr_person_ids)
                    self.destination_addr_person_ids = persons
                    _logger.info(u'>>>>>>>>>> %s', self.destination_addr_person_ids)

        # return True
        return self._reopen_form()

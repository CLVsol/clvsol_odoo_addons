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


class AnimalHistoryUpdate(models.TransientModel):
    _name = 'clv.animal.history_updt'

    def _default_animal_ids(self):
        return self._context.get('active_ids')
    animal_ids = fields.Many2many(
        comodel_name='clv.animal',
        relation='clv_animal_history_updt_rel',
        string='Animals',
        default=_default_animal_ids
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
    def do_animal_history_updt(self):
        self.ensure_one()

        AnimalHistory = self.env['clv.animal.history']

        for animal in self.animal_ids:

            if self.sign_out_date is False:
                raise exceptions.ValidationError('The "Sign out date" has not been defined!')
                return self._reopen_form()

            if self.sign_in_date is False:
                raise exceptions.ValidationError('The "Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s', '>>>>>', animal.name)

            if animal.history_marker_id.id is not False:

                animal_history = AnimalHistory.search([
                    ('animal_id', '=', animal.id),
                    ('history_marker_id', '=', animal.history_marker_id.id),
                    ('sign_out_date', '=', False),
                ])

                if animal_history.id is False:

                    animal_history_2 = AnimalHistory.search([
                        ('animal_id', '=', animal.id),
                        ('sign_out_date', '=', False),
                    ])
                    if animal_history_2.id is not False:
                        animal_history_2.sign_out_date = self.sign_out_date
                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', animal_history_2.history_marker_id.name,
                                                     animal_history_2.sign_in_date,
                                                     animal_history_2.sign_out_date)

                    m2m_list = []
                    for category_id in animal.category_ids:
                        m2m_list.append((4, category_id.id))
                    category_ids = m2m_list
                    values = {
                        'animal_id': animal.id,
                        'category_ids': category_ids,
                        'date_reference': animal.date_reference,
                        'age_reference': animal.age_reference,
                        'estimated_age': animal.estimated_age,
                        'tutor_id': animal.tutor_id.id,
                        'address_id': animal.address_id.id,
                        'sign_in_date': self.sign_in_date,
                        'history_marker_id': animal.history_marker_id.id,
                    }
                    animal_history = AnimalHistory.create(values)
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', animal_history.history_marker_id.name,
                                                 animal_history.sign_in_date,
                                                 animal_history.sign_out_date)

                else:
                    m2m_list = []
                    for category_id in animal.category_ids:
                        m2m_list.append((4, category_id.id))
                    m2m_list_2 = []
                    for category_id in animal_history.category_ids:
                        m2m_list_2.append((4, category_id.id))
                    if m2m_list != m2m_list_2:
                        animal_history.category_ids = m2m_list
                    if animal_history.date_reference != animal.date_reference:
                        animal_history.date_reference = animal.date_reference
                    if animal_history.age_reference != animal.age_reference:
                        animal_history.age_reference = animal.age_reference
                    if animal_history.estimated_age != animal.estimated_age:
                        animal_history.estimated_age = animal.estimated_age
                    if animal_history.tutor_id.id != animal.tutor_id.id:
                        animal_history.tutor_id = animal.tutor_id.id
                    if animal_history.address_id.id != animal.address_id.id:
                        animal_history.address_id = animal.address_id.id
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', animal_history.history_marker_id.name,
                                                 animal_history.sign_in_date,
                                                 animal_history.sign_out_date)

            else:

                animal_history = AnimalHistory.search([
                    ('animal_id', '=', animal.id),
                    ('sign_out_date', '=', False),
                ])

                if animal_history.id is not False:
                    animal_history.sign_out_date = self.sign_out_date
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', animal_history.history_marker_id.name,
                                                 animal_history.sign_in_date,
                                                 animal_history.sign_out_date)

        return True

    @api.multi
    def do_populate_all_animals(self):
        self.ensure_one()

        Animal = self.env['clv.animal']
        animals = Animal.search([])

        self.animal_ids = animals

        return self._reopen_form()

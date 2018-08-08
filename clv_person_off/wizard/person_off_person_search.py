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

_logger = logging.getLogger(__name__)


class PersonOffPersonSearch(models.TransientModel):
    _name = 'clv.person.off.person_search'

    def _default_person_off_ids(self):
        return self._context.get('active_ids')
    person_off_ids = fields.Many2many(
        comodel_name='clv.person.off',
        relation='clv_person_off_person_search_rel',
        string='Persons (Off)',
        default=_default_person_off_ids
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
    def do_person_off_person_search(self):
        self.ensure_one()

        Person = self.env['clv.person']

        for person_off in self.person_off_ids:

            _logger.info(u'>>>>> %s', person_off.name)

            if (person_off.action_person in ['undefined', 'create']) and \
               (person_off.person_id.id is False):

                person = Person.search([
                    ('name', '=', person_off.name),
                ])
                if person.id is not False:

                    person_off.person_id = person.id
                    person_off.action_person = 'confirm'

                    _logger.info(u'>>>>>>>>>> %s', person_off.person_id.name)

        return True

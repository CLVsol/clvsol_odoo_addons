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


class PersonMngPersonUpdate(models.TransientModel):
    _name = 'clv.person.mng.person_update'

    def _default_person_mng_ids(self):
        return self._context.get('active_ids')
    person_mng_ids = fields.Many2many(
        comodel_name='clv.person.mng',
        relation='clv_person_mng_person_update_rel',
        string='Persons (Management)',
        default=_default_person_mng_ids
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
    def do_person_mng_person_update(self):
        self.ensure_one()

        for person_mng in self.person_mng_ids:

            _logger.info(u'>>>>> %s', person_mng.name)

            if person_mng.action_person == 'update':

                if person_mng.person_id.id is not False:

                    if person_mng.person_id.name != person_mng.name:
                        person_mng.person_id.name = person_mng.name

                    if person_mng.person_id.birthday != person_mng.birthday:
                        person_mng.person_id.birthday = person_mng.birthday

                    if person_mng.responsible_id.id is not False:
                        if person_mng.person_id.responsible_id.id is not False:
                            if person_mng.person_id.responsible_id.id != person_mng.responsible_id.id:
                                person_mng.person_id.responsible_id = person_mng.responsible_id.id
                        else:
                            person_mng.person_id.responsible_id = person_mng.responsible_id.id

                    if person_mng.caregiver_id.id is not False:
                        if person_mng.person_id.caregiver_id.id is not False:
                            if person_mng.person_id.caregiver_id.id != person_mng.caregiver_id.id:
                                person_mng.person_id.caregiver_id = person_mng.caregiver_id.id
                        else:
                            person_mng.person_id.caregiver_id = person_mng.caregiver_id.id

                    _logger.info(u'>>>>>>>>>> %s: %s', 'action_person', person_mng.action_person)

                    person_mng.action_person = 'confirm'

        return True

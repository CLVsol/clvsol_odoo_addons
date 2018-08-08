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


class PersonOffUpdateData(models.TransientModel):
    _name = 'clv.person.off.update_data'

    def _default_person_off_ids(self):
        return self._context.get('active_ids')
    person_off_ids = fields.Many2many(
        comodel_name='clv.person.off',
        relation='clv_person_off_update_data_rel',
        string='Persons (Management)',
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
    def do_person_off_update_data(self):
        self.ensure_one()

        for person_off in self.person_off_ids:

            _logger.info(u'>>>>> %s', person_off.name)

            if (person_off.state in ['draft', 'revised']) and \
               (person_off.person_id.id is not False):

                person_off.name = person_off.person_id.name
                person_off.code = person_off.person_id.code
                person_off.gender = person_off.person_id.gender
                person_off.birthday = person_off.person_id.birthday
                person_off.birthday = person_off.person_id.birthday
                person_off.responsible_id = person_off.person_id.responsible_id.id
                person_off.caregiver_id = person_off.person_id.caregiver_id.id

                if person_off.person_id.address_id.id is not False:

                    person_off.street = person_off.person_id.address_id.street
                    person_off.street2 = person_off.person_id.address_id.street2
                    person_off.zip = person_off.person_id.address_id.zip
                    person_off.city = person_off.person_id.address_id.city
                    person_off.state_id = person_off.person_id.address_id.state_id.id
                    person_off.country_id = person_off.person_id.address_id.country_id.id
                    person_off.phone = person_off.person_id.address_id.phone
                    person_off.mobile = person_off.person_id.address_id.mobile

        return True

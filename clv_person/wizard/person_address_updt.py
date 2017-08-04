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


class PersonAddressUpdt(models.TransientModel):
    _name = 'clv.person.address_updt'

    def _default_person_ids(self):
        return self._context.get('active_ids')
    person_ids = fields.Many2many(
        comodel_name='clv.person',
        relation='clv_person_address_updt_rel',
        string='Persons to Update',
        default=_default_person_ids)
    count_persons = fields.Integer(
        string='Number of Persons',
        compute='_compute_count_persons',
        store=False
    )
    check_current_address = fields.Boolean(string='Check current Address', default=1)

    new_address_id = fields.Many2one(
        comodel_name='clv.address',
        string='New Address'
    )
    new_address_code = fields.Char(
        string='New Address Code',
        related='new_address_id.code',
        store=False,
        readonly=True
    )
    new_address_category_ids = fields.Char(
        string='New Address Categories',
        related='new_address_id.category_ids.name',
        store=False,
        readonly=True
    )
    # new_address_state = fields.Selection(
    #     string='New Address State',
    #     related='new_address_id.state',
    #     store=False,
    #     readonly=True
    # )

    @api.depends('person_ids')
    def _compute_count_persons(self):
        for r in self:
            r.count_persons = len(r.person_ids)

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
    def do_person_address_updt(self):
        self.ensure_one()

        if self.check_current_address:
            current_address_id = False
            for person_reg in self.person_ids:
                if current_address_id is False:
                    current_address_id = person_reg.address_id.id
                else:
                    if person_reg.address_id.id != current_address_id:
                        raise exceptions.ValidationError('Current Address is not the same for all Persons!')

        _logger.warning(u'Person Address Update on %s', self.person_ids.ids)

        for person_reg in self.person_ids:

            _logger.info(u'%s %s', person_reg.id, person_reg.name)

            if self.new_address_id:
                person_reg.address_id = self.new_address_id

        # return True
        return self._reopen_form()

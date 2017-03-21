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

from datetime import *

from odoo import api, fields, models


class PersonAddressHistory(models.Model):
    _description = 'Person Address History'
    _name = 'clv.person.address.history'
    _order = "sign_in_date desc"

    person_id = fields.Many2one(
        comodel_name='clv.person',
        string='Person',
        required=False
    )
    address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Address',
        required=False
    )
    role_id = fields.Many2one(
        comodel_name='clv.person.address.role',
        string='Role',
        required=False
    )
    sign_in_date = fields.Date(
        string='Sign in date',
        required=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    sign_out_date = fields.Date(
        string="Sign out date",
        required=False
    )

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)


class Person(models.Model):
    _inherit = 'clv.person'

    person_address_history_ids = fields.One2many(
        comodel_name='clv.person.address.history',
        inverse_name='person_id',
        string='Addresses'
    )


class Address(models.Model):
    _inherit = 'clv.address'

    person_address_history_ids = fields.One2many(
        comodel_name='clv.person.address.history',
        inverse_name='address_id',
        string='Person Addresses'
    )
    count_person_addresses = fields.Integer(
        string='Number of Person Addresses',
        compute='_compute_count_person_addresses',
        store=False
    )

    @api.depends('person_address_history_ids')
    def _compute_count_person_addresses(self):
        for r in self:
            r.count_person_addresses = len(r.person_address_history_ids)

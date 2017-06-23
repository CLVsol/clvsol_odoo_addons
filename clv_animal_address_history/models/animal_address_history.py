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


class AnimalAddressHistory(models.Model):
    _description = 'Animal Address History'
    _name = 'clv.animal.address.history'
    _order = "sign_in_date desc"

    animal_id = fields.Many2one(
        comodel_name='clv.animal',
        string='Animal',
        required=False
    )
    address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Address',
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


class Animal(models.Model):
    _inherit = 'clv.animal'

    animal_address_history_ids = fields.One2many(
        comodel_name='clv.animal.address.history',
        inverse_name='animal_id',
        string='Addresses'
    )


class Address(models.Model):
    _inherit = 'clv.address'

    animal_address_history_ids = fields.One2many(
        comodel_name='clv.animal.address.history',
        inverse_name='address_id',
        string='Animal Addresses'
    )
    count_animal_addresses = fields.Integer(
        string='Number of Animal Addresses',
        compute='_compute_count_animal_addresses',
        store=False
    )

    @api.depends('animal_address_history_ids')
    def _compute_count_animal_addresses(self):
        for r in self:
            r.count_animal_addresses = len(r.animal_address_history_ids)

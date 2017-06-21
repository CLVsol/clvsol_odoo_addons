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

from odoo import api, fields, models


class Address(models.Model):
    _inherit = 'clv.address'

    animal_ids = fields.One2many(
        comodel_name='clv.animal',
        inverse_name='address_id',
        string='Animals'
    )
    count_animals = fields.Integer(
        string='Number of Animals',
        compute='_compute_count_animals',
        store=True
    )

    @api.depends('animal_ids')
    def _compute_count_animals(self):
        for r in self:
            r.count_animals = len(r.animal_ids)


class Animal(models.Model):
    _inherit = 'clv.animal'

    address_id = fields.Many2one(comodel_name='clv.address', string='Address', ondelete='restrict')
    address_code = fields.Char(string='Address Code', related='address_id.code', store=False)

    address_phone = fields.Char(string='Address Phone', related='address_id.phone')
    address_mobile_phone = fields.Char(string='Address Mobile', related='address_id.mobile')
    address_email = fields.Char(string='Address Email', related='address_id.email')

    address_category_ids = fields.Char(
        string='Address Categories',
        related='address_id.category_ids.name',
        store=True
    )

    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')

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

    person_ids = fields.One2many(
        comodel_name='clv.person',
        inverse_name='address_id',
        string='Persons'
    )
    count_persons = fields.Integer(
        string='Number of Persons',
        compute='_compute_count_persons',
        store=True
    )

    @api.depends('person_ids')
    def _compute_count_persons(self):
        for r in self:
            r.count_persons = len(r.person_ids)


class Person(models.Model):
    _inherit = 'clv.person'

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
    address_state = fields.Selection(string='Address Status', related='address_id.state', store=True)

    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')

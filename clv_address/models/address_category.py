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

from openerp import fields, models


class Address(models.Model):
    _inherit = "clv.address"

    category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        relation='clv_address_category_rel',
        column1='address_id',
        column2='category_id',
        string='Categories'
    )
    category_names = fields.Char(string='Categories', related='category_ids.name', store=True)


class AddressCategory(models.Model):
    _description = 'Address Category'
    _name = 'clv.address.category'
    _inherit = 'clv.object.category'

    code = fields.Char(string='Category Code', required=False)

    parent_id = fields.Many2one(
        comodel_name='clv.address.category',
        string='Parent Category',
        index=True,
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='clv.address.category',
        inverse_name='parent_id',
        string='Child Categories'
    )

    address_ids = fields.Many2many(
        comodel_name='clv.address',
        string='Addresses'
    )

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

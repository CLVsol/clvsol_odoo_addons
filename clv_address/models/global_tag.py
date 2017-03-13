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

from odoo import models, fields


class Address(models.Model):
    _inherit = 'clv.address'

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_address_global_tag_rel',
        column1='address_id',
        column2='global_tag_id',
        string='Global Tags'
    )
    global_tag_names = fields.Char(string='Global Tags', related='global_tag_ids.name', store=True)


class Tag(models.Model):
    _inherit = 'clv.global_tag'

    address_ids = fields.Many2many(
        comodel_name='clv.address',
        relation='clv_address_global_tag_rel',
        column1='address_id',
        column2='global_tag_id',
        string='Addresses'
    )

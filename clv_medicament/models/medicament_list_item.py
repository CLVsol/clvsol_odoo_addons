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

from odoo import fields, models


class MedicamentListItem(models.Model):
    _description = 'Medicament List Item'
    _name = 'clv.medicament.list.item'
    _order = 'order'

    medicament_list_id = fields.Many2one(
        comodel_name='clv.medicament.list',
        string='Medicament List',
        help='Medicament List',
        required=False
    )
    medicament_id = fields.Many2one(
        comodel_name='clv.medicament',
        string='Medicament',
        help='Medicament',
        required=False
    )

    notes = fields.Text(string='Notes')

    order = fields.Integer(string='Order', default=10)

    active = fields.Boolean(string='Active', default=1)


class MedicamentList(models.Model):
    _inherit = 'clv.medicament.list'

    abcfarma_list_item_ids = fields.One2many(
        comodel_name='clv.medicament.list.item',
        inverse_name='medicament_list_id',
        string='Medicament List Itens'
    )

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

from datetime import datetime

from odoo import api, fields, models


class MedicamentModel(models.AbstractModel):
    _name = 'clv.medicament.model'
    _order = 'name'

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s {%s}' % (record.name, record.code)
                 ))
        return result

    name = fields.Char(string='Product Name', index=True, required=True)

    code = fields.Char(string='Medicament Code', required=False)

    medicament_name = fields.Char(string='Medicament Name')

    presentation = fields.Char(string='Presentation')

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Date(
        string='Inclusion Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    active = fields.Boolean(string='Active', default=1)

    is_product = fields.Boolean(
        string='Is a Product',
        help="Check if the medicament is a product.",
        default=False
    )

    is_fraction = fields.Boolean(
        string='Is a Fraction',
        help="Check if the medicament is a fraction of a product.",
        default=False
    )

    for_hospital_use = fields.Boolean(
        string='For Hospital Use',
        help="Check if for hospital use only.",
        default=False)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]


class MedicamentModel_2(models.AbstractModel):
    _inherit = 'clv.medicament.model'

    active_component_id = fields.Many2one(
        comodel_name='clv.medicament.active_component',
        string='Active Component',
        help='Medicament Active Component'
    )
    concentration = fields.Char(string='Concentration')


class MedicamentActiveComponent(models.Model):
    _inherit = 'clv.medicament.active_component'

    medicament_ids = fields.One2many(
        comodel_name='clv.medicament',
        inverse_name='active_component_id',
        string='Medicaments'
    )

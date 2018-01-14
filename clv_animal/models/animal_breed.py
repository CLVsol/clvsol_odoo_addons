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


class AnimalBreed(models.Model):
    _description = 'Animal Breed'
    _name = 'clv.animal.breed'
    _order = 'name'

    name = fields.Char(string='Breed', required=True)

    code = fields.Char(string='Breed Code', required=False)

    species_id = fields.Many2one(comodel_name='clv.animal.species', string='Species', ondelete='restrict')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE(species_id, name)',
         u'Error! The Animal Species must be unique!'
         ),
        ('code_uniq',
         'UNIQUE(code)',
         u'Error! The Animal Code must be unique!'
         ),
    ]


class Animal(models.Model):
    _inherit = 'clv.animal'

    breed_id = fields.Many2one(
        comodel_name='clv.animal.breed',
        string='Breed',
        ondelete='restrict',
        domain="[('species_id','=',species_id)]"
    )


class AnimalSpecies_2(models.Model):
    _inherit = 'clv.animal.species'

    breed_ids = fields.One2many(
        comodel_name='clv.animal.breed',
        inverse_name='species_id',
        string='Breeds'
    )


class AnimalBreed_2(models.Model):
    _inherit = 'clv.animal.breed'

    animal_ids = fields.One2many(
        comodel_name='clv.animal',
        inverse_name='breed_id',
        string='Animals'
    )

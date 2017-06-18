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


class LabTestUnit(models.Model):
    _description = 'Lab Test Unit'
    _name = "clv.lab_test.unit"

    name = fields.Char(
        string='Unit',
        required=True,
        help='Unit for Lab Test Criteria'
    )
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),

        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

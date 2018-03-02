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

from odoo import fields, models


class MedicamentList(models.Model):
    _description = 'Medicament List'
    _name = 'clv.medicament.list'
    _order = 'name'

    name = fields.Char(string='Medicament List', required=True)

    code = fields.Char(string='Medicament List Code', required=False)

    description = fields.Char(string='Description')
    notes = fields.Text(string='Notes')

    date_inclusion = fields.Date(
        string='Inclusion Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The List Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The List Code must be unique!'),
    ]

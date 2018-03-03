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


class Card(models.Model):
    _description = 'Card'
    _name = 'clv.card'

    @api.multi
    @api.depends('name', 'printed_code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s]' % (record.name, record.printed_code)
                 ))
        return result

    name = fields.Char(string='Printed Name', required=True)
    printed_code = fields.Char(string='Printed Code', required=False)

    code = fields.Char(string='Card Code', required=False)
    sequence_code = fields.Char(string='Sequence Code', required=False)

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string="Inclusion Date", required=False, readonly=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    date_valid_from = fields.Date(
        string="Valid-from Date", required=False, readonly=False
    )
    date_valid_until = fields.Date(
        string="Valid-until Date", required=False, readonly=False
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_sequence_uniq',
         'UNIQUE(code, sequence_code)',
         u'Error! The Card Code-Sequence must be unique!'
         )
    ]

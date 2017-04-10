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


class Community(models.Model):
    _description = 'Community'
    _name = 'clv.community'
    _order = 'name'

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s]' % (record.name, record.code)
                 ))
        return result

    name = fields.Char(string='Community Name', required=True, help="Community Name")
    alias = fields.Char('Community Alias', help='Common name that the Community is referred')

    code = fields.Char(string='Community Code', required=False)

    comm_location = fields.Char('Community Location')

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Date(
        string='Inclusion Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Community Responsible'
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

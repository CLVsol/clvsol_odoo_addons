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


class ExternalSyncHost(models.Model):
    _description = 'External Sync Host'
    _name = 'clv.external_sync.host'
    _order = 'name'

    name = fields.Char(
        string='External Host Name',
        required=True,
        help='External Sync Host Name (Example: http://localhost:8069'
    )

    external_dbname = fields.Char(
        string='External Database Name',
        help='External Database Name'
    )
    external_user = fields.Char(
        string='External User',
        help='External Sync User'
    )
    external_user_pw = fields.Char(
        string='External User Password',
        help='External Sync User Password'
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
    ]

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

from odoo import api, fields, models


class Event(models.Model):
    _description = 'Event'
    _name = 'clv.event'
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

    name = fields.Char(string='Event Name', required=True, help="Event Name")

    code = fields.Char(string='Event Code', required=False)

    sequence = fields.Integer(
        string='Sequence', index=True, default=10,
        help="Gives the sequence order when displaying a list of events.")
    planned_hours = fields.Float(
        string='Planned Hours',
        help='Estimated time (in hours) to do the event.'
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)
    date_foreseen = fields.Datetime(string='Foreseen Date', index=True, copy=False)
    date_start = fields.Datetime(string='Starting Date', index=True, copy=False)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False)

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

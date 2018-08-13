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

from datetime import *

from odoo import api, fields, models


class AbstractLog(models.AbstractModel):
    _name = 'clv.abstract.log'
    _order = "id desc"

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        required=True,
        default=lambda self: self.env.user
    )
    date_log = fields.Datetime(
        string='When',
        required=True,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    values = fields.Text(string='Values')
    action = fields.Char(string='Action')
    notes = fields.Text(string='Notes')


class LogModel(models.AbstractModel):
    _name = 'clv.log.model'

    active_log = fields.Boolean(
        string='Active Log',
        help="If unchecked, it will allow you to disable the log without removing it.",
        default=True
    )

    @api.multi
    def write(self, values):
        action = 'write'
        notes = False
        for record in self:
            record.insert_object_log(record.id, values, action, notes)
        return super(LogModel, self).write(values)

    @api.model
    def create(self, values):
        action = 'create'
        notes = False
        record = super(LogModel, self).create(values)
        record.insert_object_log(record.id, values, action, notes)
        return record

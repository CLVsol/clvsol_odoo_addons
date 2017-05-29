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


class Document(models.Model):
    _description = 'Document'
    _name = 'clv.document'
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

    name = fields.Char(string='Document Name', required=True, help="Document Name")

    code = fields.Char(string='Document Code', required=False)

    base_document_id = fields.Many2one(
        comodel_name='clv.document',
        string='Base Document',
        required=False,
        help="Base Document"
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Document Responsible',
        required=False,
        help='Document Responsible',
    )

    notes = fields.Text(string='Notes')

    date_requested = fields.Date(
        string='Date requested',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    date_document = fields.Date(string='Document Date')
    date_foreseen = fields.Date(string='Foreseen Date', index=True, copy=False)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False)

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

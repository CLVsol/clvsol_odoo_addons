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


class DocumentOff(models.Model):
    _description = 'Document Off'
    _name = 'clv.document.off'
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

    name = fields.Char(string='Document (Off) Name', required=True, help="Document (Off) Name")

    code = fields.Char(string='Document (Off) Code', required=False)

    # base_document_id = fields.Many2one(
    #     comodel_name='clv.document.off',
    #     string='Base Document (Off)',
    #     required=False,
    #     help="Base Document (Off)"
    # )

    notes = fields.Text(string='Notes')

    date_requested = fields.Date(
        string='Date requested',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    date_document_off = fields.Date(string='Document (Off) Date')
    # date_foreseen = fields.Date(string='Foreseen Date', index=True, copy=False)
    # date_deadline = fields.Date(string='Deadline', index=True, copy=False)

    document_id = fields.Many2one(
        comodel_name='clv.document',
        string='Related Document',
        ondelete='restrict'
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

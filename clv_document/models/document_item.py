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


class DocumentItem(models.Model):
    _description = 'Document Item'
    _name = "clv.document.item"
    _order = "sequence"

    code = fields.Char(string='Item Code')
    name = fields.Char(string='Item')

    value = fields.Char(sring='Value')

    document_type_id = fields.Many2one(comodel_name='clv.document.type', string='Item Type')

    document_id = fields.Many2one(comodel_name='clv.document', string='Document')

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )

    document_display = fields.Boolean(string='Display in Document', default=True)

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('type_code_uniq',
         'UNIQUE(document_type_id, code)',
         u'Error! The Code must be unique for a Document Type!'
         ),
        ('document_code_uniq',
         'UNIQUE(document_id, code)',
         u'Error! The Code must be unique for a Document!'
         ),
    ]


class DocumentType(models.Model):
    _inherit = 'clv.document.type'

    item_ids = fields.One2many(
        comodel_name='clv.document.item',
        inverse_name='document_type_id',
        string='Items'
    )


class Document(models.Model):
    _inherit = 'clv.document'

    item_ids = fields.One2many(
        comodel_name='clv.document.item',
        inverse_name='document_id',
        string='Items'
    )

    items_ok = fields.Boolean(string='Items Ok', default=0)

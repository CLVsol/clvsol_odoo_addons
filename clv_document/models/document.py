# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import fields, models


class Document(models.Model):
    _description = 'Document'
    _name = 'clv.document'
    _rec_name = 'code'
    _order = 'code'

    code = fields.Char(string='Document Code', required=False)

    base_document_id = fields.Many2one(
        comodel_name='clv.document',
        string='Base Document',
        required=False,
        help="Base Document"
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Date(
        string='Inclusion Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    date_document = fields.Date(string='Document Date')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

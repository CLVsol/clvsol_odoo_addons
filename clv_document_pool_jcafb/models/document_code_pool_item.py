# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentCodePoolItem(models.Model):
    _description = 'Document Code Pool Item'
    _name = 'clv.document.code_pool.item'
    _inherit = 'clv.abstract.code'
    _rec_name = 'code'
    _order = 'code'

    code = fields.Char(string='Document Code', required=False, default='/')

    # code_sequence = fields.Char(string='Code Sequence', default='clv.document.code')

    document_code_pool_id = fields.Many2one(
        comodel_name='clv.document.code_pool',
        string='Document Code Pool',
        ondelete='restrict'
    )

    document_id = fields.Many2one(
        comodel_name='clv.document',
        string='Document',
        ondelete='restrict'
    )

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         'Error! The Code must be unique!'),
    ]


class DocumentCodePool(models.Model):
    _inherit = 'clv.document.code_pool'

    item_ids = fields.One2many(
        comodel_name='clv.document.code_pool.item',
        inverse_name='document_code_pool_id',
        string='Items',
        readonly=True
    )
    count_items = fields.Integer(
        string='Number of Items',
        compute='_compute_count_items',
        store=False
    )

    @api.depends('item_ids')
    def _compute_count_items(self):
        for r in self:
            r.count_items = len(r.item_ids)

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Document(models.Model):
    _description = 'Document'
    _name = 'clv.document'
    _rec_name = 'code'
    _order = 'code'

    code = fields.Char(string='Document Code', required=False)

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Date(
        string='Inclusion Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    date_document = fields.Date(string='Document Date')

    parent_id = fields.Many2one(
        comodel_name='clv.document',
        string='Parent Document',
        index=True,
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='clv.document',
        inverse_name='parent_id',
        string='Child Documents'
    )
    count_children = fields.Integer(
        string='Documents (count)',
        compute='_compute_count_children',
        # store=True
    )

    # @api.depends('child_ids')
    def _compute_count_children(self):
        for r in self:
            r.count_children = len(r.child_ids)

    active = fields.Boolean(string='Active', default=1)

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive documnets.'))
        return True

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

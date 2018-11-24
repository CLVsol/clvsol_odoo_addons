# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    document_ids = fields.One2many(
        comodel_name='clv.document',
        inverse_name='phase_id',
        string='Documents',
        readonly=True
    )
    count_documents = fields.Integer(
        string='Documents (count)',
        compute='_compute_document_ids_and_count',
    )

    @api.multi
    def _compute_document_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            documents = self.env['clv.document'].search(search_domain)

            record.count_documents = len(documents)
            record.document_ids = [(6, 0, documents.ids)]


class Document(models.Model):
    _inherit = 'clv.document'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )
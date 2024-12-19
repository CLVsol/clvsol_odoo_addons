# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DocumentCodePoolGet(models.TransientModel):
    _description = 'Document Code Pool Get'
    _name = 'clv.document.code_pool.item_get'

    def _default_document_code_pool_ids(self):
        return self._context.get('active_ids')
    document_code_pool_ids = fields.Many2many(
        comodel_name='clv.document.code_pool',
        relation='clv_document_code_pool_document_code_pool_item_get_rel',
        string='Document Code Pools',
        default=_default_document_code_pool_ids
    )

    def do_document_code_pool_item_get(self):
        self.ensure_one()

        DocumentCodePoolItem = self.env['clv.document.code_pool.item']
        Document = self.env['clv.document']

        for document_code_pool in self.document_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', document_code_pool.name)

            documents = Document.search([])
            items = DocumentCodePoolItem.search([])

            for document in documents:

                found_item = False
                for item in items:

                    if (document.code == item.code):
                        found_item = True

                if not found_item:

                    if document.code is not False:

                        sequence_str = document.code[:7].replace('.', '')
                        format_code = self.env['clv.abstract.code'].format_code(sequence_str)

                        if document.code == format_code:

                            values = {
                                'document_code_pool_id': document_code_pool.id,
                                'code_sequence': document_code_pool.code_sequence,
                                'code': document.code,
                                'document_id': document.id,
                                'notes': 'New'
                            }

                        else:

                            values = {
                                'document_code_pool_id': document_code_pool.id,
                                'code_sequence': document_code_pool.code_sequence,
                                'code': document.code,
                                'document_id': document.id,
                                'notes': 'New (Invalid)'
                            }

                        document_code_pool_item = DocumentCodePoolItem.create(values)

                        _logger.info(u'%s %s - %s', '>>>>>>>>>>', document_code_pool_item.code, document_code_pool_item.notes)

        return True

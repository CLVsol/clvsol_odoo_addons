# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DocumentCodePoolSeek(models.TransientModel):
    _description = 'Document Code Pool Seek'
    _name = 'clv.document.code_pool.item_seek'

    def _default_document_code_pool_ids(self):
        return self._context.get('active_ids')
    document_code_pool_ids = fields.Many2many(
        comodel_name='clv.document.code_pool',
        relation='clv_document_code_pool_document_code_pool_item_seek_rel',
        string='Document Code Pools',
        default=_default_document_code_pool_ids
    )

    def do_document_code_pool_item_seek(self):
        self.ensure_one()

        DocumentCodePoolItem = self.env['clv.document.code_pool.item']
        Document = self.env['clv.document']

        for document_code_pool in self.document_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', document_code_pool.name)

            search_domain = [
                ('document_code_pool_id', '=', document_code_pool.id),
            ]
            items = DocumentCodePoolItem.search(search_domain)

            for item in items:

                if (item.document_id is not False):

                    item.document_id = False

            for item in items:

                documents = Document.search([])

                for document in documents:

                    if (document.code == item.code):

                        item.document_id = document.id

        return True

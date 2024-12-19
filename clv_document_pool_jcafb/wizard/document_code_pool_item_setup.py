# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DocumentCodePoolSetUp(models.TransientModel):
    _description = 'Document Code Pool Setup'
    _name = 'clv.document.code_pool.item_setup'

    def _default_document_code_pool_ids(self):
        return self._context.get('active_ids')
    document_code_pool_ids = fields.Many2many(
        comodel_name='clv.document.code_pool',
        relation='clv_document_code_pool_document_code_pool_item_setup_rel',
        string='Document Code Pools',
        default=_default_document_code_pool_ids
    )

    code_quantity = fields.Integer(
        string='Code Quantity',
        help="Quantity of Codes",
    )

    def _default_sequence_min(self):
        Document = self.env['clv.document']
        documents = Document.search([], order='code')
        code_min = documents[0].code
        number_min_str = code_min[2:code_min.index('-')].replace('.', '')
        number_min = int(number_min_str)
        return number_min
    sequence_min = fields.Integer(
        string='Sequence Minimum',
        help="Sequence Minimum value",
        default=_default_sequence_min
    )

    def _default_sequence_max(self):
        IrSequence = self.env['ir.sequence']
        ir_sequence = IrSequence.search([('code', '=', 'clv.document.code')])
        return ir_sequence.number_next_actual - 1
    sequence_max = fields.Integer(
        string='Sequence Maximum',
        help="Sequence Maximum value",
        default=_default_sequence_max
    )

    def do_document_code_pool_item_setup(self):
        self.ensure_one()

        DocumentCodePoolItem = self.env['clv.document.code_pool.item']

        for document_code_pool in self.document_code_pool_ids:

            _logger.info(u'%s %s (%s)', '>>>>>', document_code_pool.name, self.code_quantity)

            IrSequence = self.env['ir.sequence']
            ir_sequence = IrSequence.search([('code', '=', 'clv.document.code')])

            number_next_actual = ir_sequence.number_next_actual
            prefix = ir_sequence.prefix
            padding = ir_sequence.padding

            number = self.sequence_min
            count = 0
            while (count < self.code_quantity) and (number <= self.sequence_max):

                number_str = str(number)
                while len(number_str) < padding:
                    number_str = '0' + number_str
                sequence_str = prefix + number_str
                format_code = self.env['clv.abstract.code'].format_code(sequence_str)
                pool_item = DocumentCodePoolItem.search([('code', '=', format_code)])

                if pool_item.id is False:

                    count += 1

                    if number < number_next_actual:

                        values = {
                            'document_code_pool_id': document_code_pool.id,
                            'code_sequence': document_code_pool.code_sequence,
                            'code': format_code
                        }

                    else:

                        values = {
                            'document_code_pool_id': document_code_pool.id,
                            'code_sequence': document_code_pool.code_sequence,
                        }

                    document_code_pool_item = DocumentCodePoolItem.create(values)

                    _logger.info(u'%s %s', '>>>>>>>>>>', document_code_pool_item.code)

                number += 1

        return True

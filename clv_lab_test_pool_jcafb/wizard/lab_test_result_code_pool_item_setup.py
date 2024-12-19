# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultCodePoolSetUp(models.TransientModel):
    _description = 'Lab Test Result Code Pool Setup'
    _name = 'clv.lab_test.result.code_pool.item_setup'

    def _default_lab_test_result_code_pool_ids(self):
        return self._context.get('active_ids')
    lab_test_result_code_pool_ids = fields.Many2many(
        comodel_name='clv.lab_test.result.code_pool',
        relation='clv_lab_test_result_code_pool_code_pool_item_setup_rel',
        string='Lab Test Result Code Pools',
        default=_default_lab_test_result_code_pool_ids
    )

    code_quantity = fields.Integer(
        string='Code Quantity',
        help="Quantity of Codes",
    )

    def _default_sequence_min(self):
        LabTestResult = self.env['clv.lab_test.result']
        lab_test_results = LabTestResult.search([], order='code')
        code_min = lab_test_results[0].code
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
        ir_sequence = IrSequence.search([('code', '=', 'clv.lab_test.result.code')])
        return ir_sequence.number_next_actual - 1
    sequence_max = fields.Integer(
        string='Sequence Maximum',
        help="Sequence Maximum value",
        default=_default_sequence_max
    )

    def do_lab_test_result_code_pool_item_setup(self):
        self.ensure_one()

        LabTestResultCodePoolItem = self.env['clv.lab_test.result.code_pool.item']

        for lab_test_result_code_pool in self.lab_test_result_code_pool_ids:

            _logger.info(u'%s %s (%s)', '>>>>>', lab_test_result_code_pool.name, self.code_quantity)

            IrSequence = self.env['ir.sequence']
            ir_sequence = IrSequence.search([('code', '=', 'clv.lab_test.result.code')])

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
                pool_item = LabTestResultCodePoolItem.search([('code', '=', format_code)])

                if pool_item.id is False:

                    count += 1

                    if number < number_next_actual:

                        values = {
                            'lab_test_result_code_pool_id': lab_test_result_code_pool.id,
                            'code_sequence': lab_test_result_code_pool.code_sequence,
                            'code': format_code
                        }

                    else:

                        values = {
                            'lab_test_result_code_pool_id': lab_test_result_code_pool.id,
                            'code_sequence': lab_test_result_code_pool.code_sequence,
                        }

                    lab_test_result_code_pool_item = LabTestResultCodePoolItem.create(values)

                    _logger.info(u'%s %s', '>>>>>>>>>>', lab_test_result_code_pool_item.code)

                number += 1

        return True

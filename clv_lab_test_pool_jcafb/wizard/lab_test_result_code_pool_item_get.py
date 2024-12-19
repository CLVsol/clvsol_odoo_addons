# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultCodePoolGet(models.TransientModel):
    _description = 'Lab Test Result Code Pool Get'
    _name = 'clv.lab_test.result.code_pool.item_get'

    def _default_lab_test_result_code_pool_ids(self):
        return self._context.get('active_ids')
    lab_test_result_code_pool_ids = fields.Many2many(
        comodel_name='clv.lab_test.result.code_pool',
        relation='clv_lab_test_result_code_pool_item_get_rel',
        string='Lab Test Result Code Pools',
        default=_default_lab_test_result_code_pool_ids
    )

    def do_lab_test_result_code_pool_item_get(self):
        self.ensure_one()

        LabTestResultCodePoolItem = self.env['clv.lab_test.result.code_pool.item']
        LabTestResult = self.env['clv.lab_test.result']

        for lab_test_result_code_pool in self.lab_test_result_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', lab_test_result_code_pool.name)

            lab_test_results = LabTestResult.search([])
            items = LabTestResultCodePoolItem.search([])

            for lab_test_result in lab_test_results:

                found_item = False
                for item in items:

                    if (lab_test_result.code == item.code):
                        found_item = True

                if not found_item:

                    if lab_test_result.code is not False:

                        sequence_str = lab_test_result.code[:7].replace('.', '')
                        format_code = self.env['clv.abstract.code'].format_code(sequence_str)

                        if lab_test_result.code == format_code:

                            values = {
                                'lab_test_result_code_pool_id': lab_test_result_code_pool.id,
                                'code_sequence': lab_test_result_code_pool.code_sequence,
                                'code': lab_test_result.code,
                                'lab_test_result_id': lab_test_result.id,
                                'notes': 'New'
                            }

                        else:

                            values = {
                                'lab_test_result_code_pool_id': lab_test_result_code_pool.id,
                                'code_sequence': lab_test_result_code_pool.code_sequence,
                                'code': lab_test_result.code,
                                'lab_test_result_id': lab_test_result.id,
                                'notes': 'New (Invalid)'
                            }

                        lab_test_result_code_pool_item = LabTestResultCodePoolItem.create(values)

                        _logger.info(u'%s %s - %s', '>>>>>>>>>>',
                                     lab_test_result_code_pool_item.code,
                                     lab_test_result_code_pool_item.notes)

        return True

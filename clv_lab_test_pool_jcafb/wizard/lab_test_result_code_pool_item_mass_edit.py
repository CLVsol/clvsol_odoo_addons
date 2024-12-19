# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class LabTestResultCodePoolItemMassEdit(models.TransientModel):
    _description = 'Lab Test Result Code Pool Item Mass Edit'
    _name = 'clv.lab_test.result.code_pool.item.mass_edit'

    def _default_lab_test_result_code_pool_item_ids(self):
        return self._context.get('active_ids')
    lab_test_result_code_pool_item_ids = fields.Many2many(
        comodel_name='clv.lab_test.result.code_pool.item',
        relation='clv_lab_test_result_code_pool_item_mass_edit_rel',
        string='Lab Test Result Code Pool Items',
        default=_default_lab_test_result_code_pool_item_ids
    )

    lab_test_result_code_pool_id = fields.Many2one(
        comodel_name='clv.lab_test.result.code_pool',
        string='Lab Test Result Code Pool'
    )
    lab_test_result_code_pool_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Lab Test Result Code Pool:', default=False, readonly=False, required=False
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        return defaults

    def do_lab_test_result_code_pool_item_mass_edit(self):
        self.ensure_one()

        for lab_test_result_code_pool_item in self.lab_test_result_code_pool_item_ids:

            _logger.info(u'%s %s', '>>>>>', lab_test_result_code_pool_item.code)

            if self.lab_test_result_code_pool_id_selection == 'set':
                lab_test_result_code_pool_item.lab_test_result_code_pool_id = self.lab_test_result_code_pool_id
            if self.lab_test_result_code_pool_id_selection == 'remove':
                lab_test_result_code_pool_item.lab_test_result_code_pool_id = False

        return True

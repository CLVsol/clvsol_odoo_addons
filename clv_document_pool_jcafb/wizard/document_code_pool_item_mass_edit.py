# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class DocumentCodePoolItemMassEdit(models.TransientModel):
    _description = 'Document Code Pool Item Mass Edit'
    _name = 'clv.document.code_pool.item.mass_edit'

    def _default_document_code_pool_item_ids(self):
        return self._context.get('active_ids')
    document_code_pool_item_ids = fields.Many2many(
        comodel_name='clv.document.code_pool.item',
        relation='clv_document_code_pool_item_mass_edit_rel',
        string='Document Code Pool Items',
        default=_default_document_code_pool_item_ids
    )

    document_code_pool_id = fields.Many2one(
        comodel_name='clv.document.code_pool',
        string='Document Code Pool'
    )
    document_code_pool_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Document Code Pool:', default=False, readonly=False, required=False
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        return defaults

    def do_document_code_pool_item_mass_edit(self):
        self.ensure_one()

        for document_code_pool_item in self.document_code_pool_item_ids:

            _logger.info(u'%s %s', '>>>>>', document_code_pool_item.code)

            if self.document_code_pool_id_selection == 'set':
                document_code_pool_item.document_code_pool_id = self.document_code_pool_id
            if self.document_code_pool_id_selection == 'remove':
                document_code_pool_item.document_code_pool_id = False

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResidenceCodePoolItemMassEdit(models.TransientModel):
    _description = 'Residence Code Pool Item Mass Edit'
    _name = 'clv.residence.code_pool.item.mass_edit'

    def _default_residence_code_pool_item_ids(self):
        return self._context.get('active_ids')
    residence_code_pool_item_ids = fields.Many2many(
        comodel_name='clv.residence.code_pool.item',
        relation='clv_residence_code_pool_item_mass_edit_rel',
        string='Residence Code Pool Items',
        default=_default_residence_code_pool_item_ids
    )

    residence_code_pool_id = fields.Many2one(
        comodel_name='clv.residence.code_pool',
        string='Residence Code Pool'
    )
    residence_code_pool_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Residence Code Pool:', default=False, readonly=False, required=False
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        return defaults

    def do_residence_code_pool_item_mass_edit(self):
        self.ensure_one()

        for residence_code_pool_item in self.residence_code_pool_item_ids:

            _logger.info(u'%s %s', '>>>>>', residence_code_pool_item.code)

            if self.residence_code_pool_id_selection == 'set':
                residence_code_pool_item.residence_code_pool_id = self.residence_code_pool_id
            if self.residence_code_pool_id_selection == 'remove':
                residence_code_pool_item.residence_code_pool_id = False

        return True

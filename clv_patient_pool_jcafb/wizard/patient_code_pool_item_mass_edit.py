# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PatientCodePoolItemMassEdit(models.TransientModel):
    _description = 'Patient Code Pool Item Mass Edit'
    _name = 'clv.patient.code_pool.item.mass_edit'

    def _default_patient_code_pool_item_ids(self):
        return self._context.get('active_ids')
    patient_code_pool_item_ids = fields.Many2many(
        comodel_name='clv.patient.code_pool.item',
        relation='clv_patient_code_pool_item_mass_edit_rel',
        string='Patient Code Pool Items',
        default=_default_patient_code_pool_item_ids
    )

    patient_code_pool_id = fields.Many2one(
        comodel_name='clv.patient.code_pool',
        string='Patient Code Pool'
    )
    patient_code_pool_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Patient Code Pool:', default=False, readonly=False, required=False
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        return defaults

    def do_patient_code_pool_item_mass_edit(self):
        self.ensure_one()

        for patient_code_pool_item in self.patient_code_pool_item_ids:

            _logger.info(u'%s %s', '>>>>>', patient_code_pool_item.code)

            if self.patient_code_pool_id_selection == 'set':
                patient_code_pool_item.patient_code_pool_id = self.patient_code_pool_id
            if self.patient_code_pool_id_selection == 'remove':
                patient_code_pool_item.patient_code_pool_id = False

        return True

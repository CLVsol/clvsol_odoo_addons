# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ExternalSyncBatchMemberMassEdit(models.TransientModel):
    _description = 'External Sync Batch Member Mass Edit'
    _name = 'clv.external_sync.batch.member.mass_edit'

    def _default_external_sync_batch_member_ids(self):
        return self._context.get('active_ids')
    external_sync_batch_member_ids = fields.Many2many(
        comodel_name='clv.external_sync.batch.member',
        relation='clv_external_sync_batch_member_mass_edit_rel',
        string='External Sync Batch Members',
        default=_default_external_sync_batch_member_ids
    )

    enabled = fields.Boolean(
        string='Enabled'
    )
    enabled_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Enabled:', default=False, readonly=False, required=False
    )

    def do_external_sync_batch_member_mass_edit(self):
        self.ensure_one()

        for external_sync_batch_member in self.external_sync_batch_member_ids:

            _logger.info(u'%s %s', '>>>>>', external_sync_batch_member.enabled)

            if self.enabled_selection == 'set':
                external_sync_batch_member.enabled = self.enabled
            if self.enabled_selection == 'remove':
                external_sync_batch_member.enabled = False

        return True

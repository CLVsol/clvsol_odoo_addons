# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ExternalSyncMassEdit(models.TransientModel):
    _description = 'External Sync Mass Edit'
    _name = 'clv.external_sync.mass_edit'

    def _default_external_sync_ids(self):
        return self._context.get('active_ids')
    external_sync_ids = fields.Many2many(
        comodel_name='clv.external_sync',
        relation='clv_external_sync_mass_edit_rel',
        string='External Syncs',
        default=_default_external_sync_ids
    )

    external_sync_state = fields.Selection(
        [('identified', 'Identified'),
         ('included', 'Included'),
         ('updated', 'Updated'),
         ('synchronized', 'Synchronized'),
         ('recognized', 'Recognized'),
         ('missing', 'Missing'),
         ], 'External Synchronization State'
    )
    external_sync_state_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='External Synchronization State:', default=False, readonly=False, required=False
    )

    def do_external_sync_mass_edit(self):
        self.ensure_one()

        for external_sync in self.external_sync_ids:

            _logger.info(u'%s %s', '>>>>>', external_sync.reference)

            if self.external_sync_state_selection == 'set':
                external_sync.external_sync_state = self.external_sync_state
            if self.external_sync_state_selection == 'remove':
                external_sync.external_sync_state = False

        return True

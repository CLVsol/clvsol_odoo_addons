# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class VerificationBatchMemberMassEdit(models.TransientModel):
    _description = 'Verification Batch Member Mass Edit'
    _name = 'clv.verification.batch.member.mass_edit'

    def _default_verification_batch_member_ids(self):
        return self._context.get('active_ids')
    verification_batch_member_ids = fields.Many2many(
        comodel_name='clv.verification.batch.member',
        relation='clv_verification_batch_member_mass_edit_rel',
        string='Verification Batch Members',
        default=_default_verification_batch_member_ids
    )

    enabled = fields.Boolean(
        string='Enabled'
    )
    enabled_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Enabled:', default=False, readonly=False, required=False
    )

    def do_verification_batch_member_mass_edit(self):
        self.ensure_one()

        for verification_batch_member in self.verification_batch_member_ids:

            _logger.info(u'%s %s', '>>>>>', verification_batch_member.enabled)

            if self.enabled_selection == 'set':
                verification_batch_member.enabled = self.enabled
            if self.enabled_selection == 'remove':
                verification_batch_member.enabled = False

        return True

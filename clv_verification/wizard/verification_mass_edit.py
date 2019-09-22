# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class VerificationMassEdit(models.TransientModel):
    _description = 'Verification Mass Edit'
    _name = 'clv.verification.mass_edit'

    def _default_verification_ids(self):
        return self._context.get('active_ids')
    verification_ids = fields.Many2many(
        comodel_name='clv.verification',
        relation='clv_verification_mass_edit_rel',
        string='Verifications',
        default=_default_verification_ids
    )

    state = fields.Selection(
        [('unknown', 'Unknown'),
         ('updated', 'Updated'),
         ('warned', 'Warned'),
         ('failed', 'Failed'),
         ('ok', 'Ok'),
         ('missing', 'Missing'),
         ], 'State'
    )
    state_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='State:', default=False, readonly=False, required=False
    )

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_verification_mass_edit(self):
        self.ensure_one()

        for verification in self.verification_ids:

            _logger.info(u'%s %s', '>>>>>', verification.reference)

            if self.state_selection == 'set':
                verification.state = self.state
            if self.state_selection == 'remove':
                verification.state = False

        return True

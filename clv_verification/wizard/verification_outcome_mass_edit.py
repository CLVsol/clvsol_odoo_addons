# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class VerificationOutcomeMassEdit(models.TransientModel):
    _description = 'Verification Outcome Mass Edit'
    _name = 'clv.verification.outcome.mass_edit'

    def _default_verification_outcome_ids(self):
        return self._context.get('active_ids')
    verification_outcome_ids = fields.Many2many(
        comodel_name='clv.verification.outcome',
        relation='clv_verification_outcome_mass_edit_rel',
        string='Verification Outcomes',
        default=_default_verification_outcome_ids
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
    def do_verification_outcome_mass_edit(self):
        self.ensure_one()

        for verification_outcome in self.verification_outcome_ids:

            _logger.info(u'%s %s', '>>>>>', verification_outcome.reference)

            if self.state_selection == 'set':
                verification_outcome.state = self.state
            if self.state_selection == 'remove':
                verification_outcome.state = False

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class VerificationTemplateMassEdit(models.TransientModel):
    _description = 'Verification Template Mas Edit'
    _name = 'clv.verification.template.mass_edit'

    def _default_verification_template_ids(self):
        return self._context.get('active_ids')
    verification_template_ids = fields.Many2many(
        comodel_name='clv.verification.template',
        relation='clv_verification_template_mass_edit_rel',
        string='Verification Templates',
        default=_default_verification_template_ids
    )

    verification_disable_identification = fields.Boolean(
        string='Disable Identification'
    )
    verification_disable_identification_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Identification:', default=False, readonly=False, required=False
    )

    verification_disable_check_missing = fields.Boolean(
        string='Disable Check Missing'
    )
    verification_disable_check_missing_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Check Missing:', default=False, readonly=False, required=False
    )

    verification_disable_inclusion = fields.Boolean(
        string='Disable Inclusion'
    )
    verification_disable_inclusion_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Inclusion:', default=False, readonly=False, required=False
    )

    verification_disable_verification = fields.Boolean(
        string='Disable Verification'
    )
    verification_disable_verification_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Verification:', default=False, readonly=False, required=False
    )

    verification_last_update_start = fields.Datetime(
        string="Last Update (Start)"
    )
    verification_last_update_start_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Last Update (Start):', default=False, readonly=False, required=False
    )

    verification_last_update_end = fields.Datetime(
        string="Last Update (End)"
    )
    verification_last_update_end_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Last Update (End):', default=False, readonly=False, required=False
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
    def do_verification_template_mass_edit(self):
        self.ensure_one()

        for verification_template in self.verification_template_ids:

            _logger.info(u'%s %s', '>>>>>', verification_template.name)

            if self.verification_disable_identification_selection == 'set':
                verification_template.verification_disable_identification = self.verification_disable_identification
            if self.verification_disable_identification_selection == 'remove':
                verification_template.verification_disable_identification = False

            if self.verification_disable_check_missing_selection == 'set':
                verification_template.verification_disable_check_missing = self.verification_disable_check_missing
            if self.verification_disable_check_missing_selection == 'remove':
                verification_template.verification_disable_check_missing = False

            if self.verification_disable_inclusion_selection == 'set':
                verification_template.verification_disable_inclusion = self.verification_disable_inclusion
            if self.verification_disable_inclusion_selection == 'remove':
                verification_template.verification_disable_inclusion = False

            if self.verification_disable_verification_selection == 'set':
                verification_template.verification_disable_verification = self.verification_disable_verification
            if self.verification_disable_verification_selection == 'remove':
                verification_template.verification_disable_verification = False

            if self.verification_last_update_start_selection == 'set':
                verification_template.verification_last_update_start = self.verification_last_update_start
            if self.verification_last_update_start_selection == 'remove':
                verification_template.verification_last_update_start = False

            if self.verification_last_update_end_selection == 'set':
                verification_template.verification_last_update_end = self.verification_last_update_end
            if self.verification_last_update_end_selection == 'remove':
                verification_template.verification_last_update_end = False

        return True

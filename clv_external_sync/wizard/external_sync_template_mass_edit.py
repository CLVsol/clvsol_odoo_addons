# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ExternalSypnTemplateMassEdit(models.TransientModel):
    _description = 'External Sync Template Mas Edit'
    _name = 'clv.external_sync.template.mass_edit'

    def _default_external_sync_template_ids(self):
        return self._context.get('active_ids')
    external_sync_template_ids = fields.Many2many(
        comodel_name='clv.external_sync.template',
        relation='clv_external_sync_template_mass_edit_rel',
        string='External Sync Templates',
        default=_default_external_sync_template_ids
    )

    external_host_id = fields.Many2one(
        comodel_name='clv.external_sync.host',
        string='External Host'
    )
    external_host_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='External Host:', default=False, readonly=False, required=False
    )

    enable_identification = fields.Boolean(
        string='Enable Identification'
    )
    enable_identification_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Enable Identification:', default=False, readonly=False, required=False
    )

    enable_check_missing = fields.Boolean(
        string='Enable Check Missing'
    )
    enable_check_missing_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Enable Check Missing:', default=False, readonly=False, required=False
    )

    enable_inclusion = fields.Boolean(
        string='Enable Inclusion'
    )
    enable_inclusion_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Enable Inclusion:', default=False, readonly=False, required=False
    )

    enable_sync = fields.Boolean(
        string='Enable Sync'
    )
    enable_sync_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Enable Sync:', default=False, readonly=False, required=False
    )

    external_last_update_start = fields.Datetime(
        string="Last Update (Start)"
    )
    external_last_update_start_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Last Update (Start):', default=False, readonly=False, required=False
    )

    external_last_update_end = fields.Datetime(
        string="Last Update (End)"
    )
    external_last_update_end_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Last Update (End):', default=False, readonly=False, required=False
    )

    def do_external_sync_template_mass_edit(self):
        self.ensure_one()

        for external_sync_template in self.external_sync_template_ids:

            _logger.info(u'%s %s', '>>>>>', external_sync_template.name)

            if self.external_host_id_selection == 'set':
                external_sync_template.external_host_id = self.external_host_id.id
            if self.external_host_id_selection == 'remove':
                external_sync_template.external_host_id = False

            if self.enable_identification_selection == 'set':
                external_sync_template.enable_identification = self.enable_identification
            if self.enable_identification_selection == 'remove':
                external_sync_template.enable_identification = False

            if self.enable_check_missing_selection == 'set':
                external_sync_template.enable_check_missing = self.enable_check_missing
            if self.enable_check_missing_selection == 'remove':
                external_sync_template.enable_check_missing = False

            if self.enable_inclusion_selection == 'set':
                external_sync_template.enable_inclusion = self.enable_inclusion
            if self.enable_inclusion_selection == 'remove':
                external_sync_template.enable_inclusion = False

            if self.enable_sync_selection == 'set':
                external_sync_template.enable_sync = self.enable_sync
            if self.enable_sync_selection == 'remove':
                external_sync_template.enable_sync = False

            if self.external_last_update_start_selection == 'set':
                external_sync_template.external_last_update_start = self.external_last_update_start
            if self.external_last_update_start_selection == 'remove':
                external_sync_template.external_last_update_start = False

            if self.external_last_update_end_selection == 'set':
                external_sync_template.external_last_update_end = self.external_last_update_end
            if self.external_last_update_end_selection == 'remove':
                external_sync_template.external_last_update_end = False

        return True

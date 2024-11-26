# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ExternalSypnScheduleMassEdit2(models.TransientModel):
    _description = 'External Sync Schedule Mass Edit (2)'
    _name = 'clv.external_sync.schedule.mass_edit_2'

    def _default_external_sync_schedule_ids(self):
        ExternalSyncBatchMember = self.env['clv.external_sync.batch.member']
        batch_member_ids = self._context.get('active_ids')
        schedule_list = []
        for batch_member_id in batch_member_ids:
            schedule = ExternalSyncBatchMember.search([
                ('id', '=', batch_member_id),
            ])
            schedule_list.append((schedule.ref_id.id))
        return schedule_list
    external_sync_schedule_ids = fields.Many2many(
        comodel_name='clv.external_sync.schedule',
        relation='clv_external_sync_schedule_mass_edit_2_rel',
        string='External Sync Schedules',
        default=_default_external_sync_schedule_ids
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

    max_task = fields.Integer(
        string='Max Task Registers'
    )
    max_task_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Max Task Registers:', default=False, readonly=False, required=False
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

    def do_external_sync_schedule_mass_edit_2(self):
        self.ensure_one()

        for external_sync_schedule in self.external_sync_schedule_ids:

            _logger.info(u'%s %s', '>>>>>', external_sync_schedule.name)

            if self.external_host_id_selection == 'set':
                external_sync_schedule.external_host_id = self.external_host_id.id
            if self.external_host_id_selection == 'remove':
                external_sync_schedule.external_host_id = False

            if self.max_task_selection == 'set':
                external_sync_schedule.max_task = self.max_task
            if self.max_task_selection == 'remove':
                external_sync_schedule.max_task = False

            if self.enable_identification_selection == 'set':
                external_sync_schedule.enable_identification = self.enable_identification
            if self.enable_identification_selection == 'remove':
                external_sync_schedule.enable_identification = False

            if self.enable_check_missing_selection == 'set':
                external_sync_schedule.enable_check_missing = self.enable_check_missing
            if self.enable_check_missing_selection == 'remove':
                external_sync_schedule.enable_check_missing = False

            if self.enable_inclusion_selection == 'set':
                external_sync_schedule.enable_inclusion = self.enable_inclusion
            if self.enable_inclusion_selection == 'remove':
                external_sync_schedule.enable_inclusion = False

            if self.enable_sync_selection == 'set':
                external_sync_schedule.enable_sync = self.enable_sync
            if self.enable_sync_selection == 'remove':
                external_sync_schedule.enable_sync = False

            if self.external_last_update_start_selection == 'set':
                external_sync_schedule.external_last_update_start = self.external_last_update_start
            if self.external_last_update_start_selection == 'remove':
                external_sync_schedule.external_last_update_start = False

            if self.external_last_update_end_selection == 'set':
                external_sync_schedule.external_last_update_end = self.external_last_update_end
            if self.external_last_update_end_selection == 'remove':
                external_sync_schedule.external_last_update_end = False

        return True

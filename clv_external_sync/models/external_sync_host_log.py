# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ExternalSyncHostLog(models.Model):
    _description = 'External Sync Host Log'
    _name = 'clv.external_sync.host.log'
    _inherit = 'clv.object.log'

    external_sync_host_id = fields.Many2one(
        comodel_name='clv.external_sync.host',
        string='External Sync Host',
        required=True,
        ondelete='cascade'
    )


class ExternalSyncHost(models.Model):
    _name = "clv.external_sync.host"
    _inherit = 'clv.external_sync.host', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.external_sync.host.log',
        inverse_name='external_sync_host_id',
        string='External Sync Host Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, external_sync_host_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'external_sync_host_id': external_sync_host_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.env['clv.external_sync.host.log'].create(vals)

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ExternalSyncBatchMember(models.Model):
    _name = "clv.external_sync.batch.member"
    _inherit = 'clv.external_sync.batch.member', 'clv.abstract.reference'

    ref_method = fields.Char(
        string='Method',
        compute='_compute_refenceable_model_schedule',
        store=True
    )

    ref_enable_identification = fields.Boolean(
        string='Enable Identification',
        compute='_compute_refenceable_model_schedule',
        store=True
    )
    ref_enable_identification_suport = fields.Boolean(
        string='Enable Identification:',
        compute='_compute_refenceable_model_schedule',
        store=False,
        compute_sudo=True
    )

    ref_enable_inclusion = fields.Boolean(
        string='Enable Inclusion',
        compute='_compute_refenceable_model_schedule',
        store=True
    )
    ref_enable_inclusion_suport = fields.Boolean(
        string='Enable Inclusion:',
        compute='_compute_refenceable_model_schedule',
        store=False,
        compute_sudo=True
    )

    ref_enable_sync = fields.Boolean(
        string='Enable Sync',
        compute='_compute_refenceable_model_schedule',
        store=True
    )
    ref_enable_sync_suport = fields.Boolean(
        string='Enable Sync:',
        compute='_compute_refenceable_model_schedule',
        store=False,
        compute_sudo=True
    )

    @api.depends('ref_id')
    def _compute_refenceable_model_schedule(self):
        for record in self:
            record.ref_method = False
            record.ref_enable_identification = False
            record.ref_enable_inclusion = False
            record.ref_enable_sync = False
            record.ref_enable_identification_suport = False
            record.ref_enable_inclusion_suport = False
            record.ref_enable_sync_suport = False
            try:
                if record.ref_id:
                    record.ref_method = record.ref_id.method
                    record.ref_enable_identification = record.ref_id.enable_identification
                    record.ref_enable_inclusion = record.ref_id.enable_inclusion
                    record.ref_enable_sync = record.ref_id.enable_sync
                    record.ref_enable_identification_suport = record.ref_id.enable_identification
                    record.ref_enable_inclusion_suport = record.ref_id.enable_inclusion
                    record.ref_enable_sync_suport = record.ref_id.enable_sync
            except Exception:
                record.ref_method = False
                record.ref_enable_identification = False
                record.ref_enable_inclusion = False
                record.ref_enable_sync = False
                record.ref_enable_identification_suport = False
                record.ref_enable_inclusion_suport = False
                record.ref_enable_sync_suport = False

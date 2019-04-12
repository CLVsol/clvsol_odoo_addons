# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DataProcessingBatchMember(models.Model):
    _description = 'Data Processing Batch Member'
    _name = 'clv.data_processing.batch.member'
    _order = "sequence"

    data_processing_batch_id = fields.Many2one(
        comodel_name='clv.data_processing.batch',
        string='Data Processing Batch ',
        required=False
    )

    notes = fields.Text(string='Notes')

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )


class DataProcessingBatch(models.Model):
    _inherit = 'clv.data_processing.batch'

    data_processing_batch_member_ids = fields.One2many(
        comodel_name='clv.data_processing.batch.member',
        inverse_name='data_processing_batch_id',
        string='Members',
        readonly=False
    )
    count_data_processing_batch_members = fields.Integer(
        string='Members (count)',
        compute='_compute_count_data_processing_batch_members',
        store=False
    )

    @api.depends('data_processing_batch_member_ids')
    def _compute_count_data_processing_batch_members(self):
        for r in self:
            r.count_data_processing_batch_members = len(r.data_processing_batch_member_ids)

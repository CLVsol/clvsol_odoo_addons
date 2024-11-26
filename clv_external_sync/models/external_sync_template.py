# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ExternalSyncTemplate(models.Model):
    _description = 'External Sync Template'
    _name = 'clv.external_sync.template'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        help='External Sync Template Name'
    )

    external_host_id = fields.Many2one(
        comodel_name='clv.external_sync.host',
        string='External Host'
    )

    max_task = fields.Integer(
        string='Max Task Registers'
    )

    enable_identification = fields.Boolean(
        string='Enable Identification',
        default=True
    )

    enable_check_missing = fields.Boolean(
        string='Enable Check Missing',
        default=True
    )

    enable_inclusion = fields.Boolean(
        string='Enable Inclusion',
        default=True
    )

    enable_sync = fields.Boolean(
        string='Enable Sync',
        default=True
    )

    force_inclusion = fields.Boolean(
        string='Force Inclusion',
        default=False
    )

    external_last_update_start = fields.Datetime(
        string="Last Update (Start)"
    )

    external_last_update_end = fields.Datetime(
        string="Last Update (End)"
    )

    apply_domain_filter = fields.Boolean(string='Apply Domain Filter', default=False)

    domain_filter = fields.Text(
        string='Domain Filter',
        required=False,
        help="Domain Filter",
        default='[]'
    )

    enable_sequence_code_sync = fields.Boolean(
        string='Enable Sequence Code Sync'
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    model = fields.Char(
        string='Model',
        required=True,
        help="Model name of the object on which the synchronization method to be called is located, e.g. 'res.partner'"
    )

    method = fields.Char(
        string='Method',
        required=True,
        help="Name of the method to be called when the synchronization job is processed."
    )

    method_args = fields.Char(
        string='Method Arguments',
        required=False,
        help="List  of arguments(Python dictionary format) for the method."
    )

    sequence_code = fields.Char(
        string='Sequence Code',
        required=False,
        help="Code of the Sequence to be synchronized when the synchronization job is processed."
    )

    external_model = fields.Char(
        string='External Model',
        required=True,
        help="External model name, e.g. 'res.partner'"
    )

    sequence_code = fields.Char(
        string='External Sequence Code',
        required=False,
        help="External Sequence Code, e.g. 'clv_address.code."
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
    ]

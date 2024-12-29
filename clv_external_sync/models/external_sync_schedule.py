# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ExternalSyncSchedule(models.Model):
    _description = 'External Sync Schedule'
    _name = 'clv.external_sync.schedule'
    _order = 'name'

    template_id = fields.Many2one(
        comodel_name='clv.external_sync.template',
        string='External Sync Template',
        required=False,
        ondelete='restrict'
    )

    name = fields.Char(
        string='Name',
        required=True,
        help='External Sync Schedule Name'
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
        required=False,
        help="Model name of the object on which the synchronization method to be called is located, e.g. 'res.partner'"
    )

    method = fields.Char(
        string='Method',
        required=False,
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
        required=False,
        help="External model name, e.g. 'res.partner'"
    )

    sequence_code = fields.Char(
        string='Sequence Code',
        required=False,
        help="Sequence Code, e.g. 'clv_address.code."
    )

    sync_log = fields.Text(
        string="Synchronization Log"
    )

    active = fields.Boolean(string='Active', default=1)

    date_last_sync = fields.Datetime(
        string='Last Synchronization Date',
        readonly=True
    )
    upmost_last_update = fields.Datetime(
        string="Upmost Last Update",
        readonly=True
    )

    # @api.model
    @api.model_create_multi
    # def create(self, values):
    def create(self, vals_list):

        # schedule = super().create(values)
        schedules = super().create(vals_list)

        # if schedule.template_id.id is not False:
        #     schedule.external_host_id = schedule.template_id.external_host_id
        #     schedule.max_task = schedule.template_id.max_task
        #     schedule.enable_identification = schedule.template_id.enable_identification
        #     schedule.enable_check_missing = schedule.template_id.enable_check_missing
        #     schedule.enable_inclusion = schedule.template_id.enable_inclusion
        #     schedule.enable_sync = schedule.template_id.enable_sync
        #     schedule.force_inclusion = schedule.template_id.force_inclusion
        #     schedule.external_last_update_start = schedule.template_id.external_last_update_start
        #     schedule.external_last_update_end = schedule.template_id.external_last_update_end
        #     schedule.apply_domain_filter = schedule.template_id.apply_domain_filter
        #     schedule.domain_filter = schedule.template_id.domain_filter
        #     schedule.enable_sequence_code_sync = schedule.template_id.enable_sequence_code_sync
        #     schedule.model = schedule.template_id.model
        #     schedule.method = schedule.template_id.method
        #     schedule.method_args = schedule.template_id.method_args
        #     schedule.sequence_code = schedule.template_id.sequence_code
        #     schedule.external_model = schedule.template_id.external_model
        #     schedule.sequence_code = schedule.template_id.sequence_code

        # ExternalSyncObjectField = self.env['clv.external_sync.object_field']
        # for object_field in schedule.template_id.object_field_ids:
        #     values = {
        #         'external_object_field': object_field.external_object_field,
        #         'local_object_field': object_field.local_object_field,
        #         'identification': object_field.identification,
        #         'inclusion': object_field.inclusion,
        #         'synchronization': object_field.synchronization,
        #         'adaptation': object_field.adaptation,
        #         'sequence': object_field.sequence,
        #         'schedule_id': schedule.id,
        #     }
        #     ExternalSyncObjectField.create(values)

        # return schedule
        for schedule in schedules:

            if schedule.template_id.id is not False:
                # schedule.external_host_id = schedule.template_id.external_host_id
                schedule.max_task = schedule.template_id.max_task
                schedule.enable_identification = schedule.template_id.enable_identification
                schedule.enable_check_missing = schedule.template_id.enable_check_missing
                schedule.enable_inclusion = schedule.template_id.enable_inclusion
                schedule.enable_sync = schedule.template_id.enable_sync
                schedule.force_inclusion = schedule.template_id.force_inclusion
                schedule.external_last_update_start = schedule.template_id.external_last_update_start
                schedule.external_last_update_end = schedule.template_id.external_last_update_end
                schedule.apply_domain_filter = schedule.template_id.apply_domain_filter
                schedule.domain_filter = schedule.template_id.domain_filter
                schedule.enable_sequence_code_sync = schedule.template_id.enable_sequence_code_sync
                schedule.model = schedule.template_id.model
                schedule.method = schedule.template_id.method
                schedule.method_args = schedule.template_id.method_args
                schedule.sequence_code = schedule.template_id.sequence_code
                schedule.external_model = schedule.template_id.external_model
                schedule.sequence_code = schedule.template_id.sequence_code

            ExternalSyncObjectField = self.env['clv.external_sync.object_field']
            for object_field in schedule.template_id.object_field_ids:
                values = {
                    'external_object_field': object_field.external_object_field,
                    'local_object_field': object_field.local_object_field,
                    'identification': object_field.identification,
                    'inclusion': object_field.inclusion,
                    'synchronization': object_field.synchronization,
                    'adaptation': object_field.adaptation,
                    'sequence': object_field.sequence,
                    'schedule_id': schedule.id,
                }
                ExternalSyncObjectField.create(values)

        return schedules

    @api.onchange('template_id')
    def onchange_template_id(self):
        ExternalSyncObjectField = self.env['clv.external_sync.object_field']
        if self.template_id.id:
            self.external_host_id = self.template_id.external_host_id
            self.max_task = self.template_id.max_task
            self.enable_identification = self.template_id.enable_identification
            self.enable_check_missing = self.template_id.enable_check_missing
            self.enable_inclusion = self.template_id.enable_inclusion
            self.enable_sync = self.template_id.enable_sync
            self.force_inclusion = self.template_id.force_inclusion
            self.external_last_update_start = self.template_id.external_last_update_start
            self.external_last_update_end = self.template_id.external_last_update_end
            self.apply_domain_filter = self.template_id.apply_domain_filter
            self.domain_filter = self.template_id.domain_filter
            self.enable_sequence_code_sync = self.template_id.enable_sequence_code_sync
            self.model = self.template_id.model
            self.method = self.template_id.method
            self.method_args = self.template_id.method_args
            self.sequence_code = self.template_id.sequence_code
            self.external_model = self.template_id.external_model
            self.sequence_code = self.template_id.sequence_code

            schedule_id = self._origin.id

            if schedule_id is not False:

                object_fields = ExternalSyncObjectField.search([
                    ('schedule_id', '=', schedule_id),
                ])
                for object_field in object_fields:
                    object_field.schedule_id = False

                for object_field in self.template_id.object_field_ids:
                    values = {
                        'external_object_field': object_field.external_object_field,
                        'local_object_field': object_field.local_object_field,
                        'identification': object_field.identification,
                        'inclusion': object_field.inclusion,
                        'synchronization': object_field.synchronization,
                        'adaptation': object_field.adaptation,
                        'sequence': object_field.sequence,
                        'schedule_id': schedule_id,
                    }
                    ExternalSyncObjectField.create(values)

    @api.model
    def external_last_update_args(self):

        args = []
        if self.external_last_update_start is not False and \
           self.external_last_update_end is False:
            args = [('write_date', '>=', self.external_last_update_start), ]
        if self.external_last_update_start is False and \
           self.external_last_update_end is not False:
            args += [('write_date', '<=', self.external_last_update_end), ]
        if self.external_last_update_start is not False and \
           self.external_last_update_end is not False:
            args += [('write_date', '>=', self.external_last_update_start),
                     ('write_date', '<=', self.external_last_update_end), ]

        return args


class ExternalSyncTemplate(models.Model):
    _inherit = 'clv.external_sync.template'

    schedule_ids = fields.One2many(
        comodel_name='clv.external_sync.schedule',
        inverse_name='template_id',
        string='Schedules'
    )
    count_schedules = fields.Integer(
        string='Number of Schedules',
        compute='_compute_count_schedules',
        store=True
    )

    @api.depends('schedule_ids')
    def _compute_count_schedules(self):
        for r in self:
            r.count_schedules = len(r.schedule_ids)

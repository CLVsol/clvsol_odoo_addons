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

    external_max_task = fields.Integer(
        string='Max Task Registers'
    )

    external_exec_sync = fields.Boolean(
        string='Execute Sync'
    )

    external_max_sync = fields.Integer(
        string='Max Sync Registers'
    )

    external_last_update_start = fields.Datetime(
        string="Last Update (Start)"
    )

    external_last_update_end = fields.Datetime(
        string="Last Update (End)"
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

    external_model = fields.Char(
        string='External Model',
        required=False,
        help="External model name, e.g. 'res.partner'"
    )

    external_sync_log = fields.Text(
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

    # _sql_constraints = [
    #     ('name_uniq',
    #      'UNIQUE (name)',
    #      u'Error! The Name must be unique!'),
    # ]

    @api.model
    def create(self, values):

        schedule = super(ExternalSyncSchedule, self).create(values)

        if schedule.template_id.id is not False:
            schedule.external_host_id = schedule.template_id.external_host_id
            schedule.external_max_task = schedule.template_id.external_max_task
            schedule.external_exec_sync = schedule.template_id.external_exec_sync
            schedule.external_max_sync = schedule.template_id.external_max_sync
            schedule.external_last_update_start = schedule.template_id.external_last_update_start
            schedule.external_last_update_end = schedule.template_id.external_last_update_end
            schedule.model = schedule.template_id.model
            schedule.method = schedule.template_id.method
            schedule.external_model = schedule.template_id.external_model

        ExternalSyncObjectField = self.env['clv.external_sync.object_field']
        for object_field in schedule.template_id.object_field_ids:
            values = {
                'external_object_field': object_field.external_object_field,
                'local_object_field': object_field.local_object_field,
                'inclusion': object_field.inclusion,
                'update': object_field.update,
                'sequence': object_field.sequence,
                'schedule_id': schedule.id,
            }
            ExternalSyncObjectField.create(values)

        return schedule

    @api.onchange('template_id')
    def onchange_template_id(self):
        ExternalSyncObjectField = self.env['clv.external_sync.object_field']
        if self.template_id.id:
            self.external_host_id = self.template_id.external_host_id
            self.external_max_task = self.template_id.external_max_task
            self.external_exec_sync = self.template_id.external_exec_sync
            self.external_max_sync = self.template_id.external_max_sync
            self.external_last_update_start = self.template_id.external_last_update_start
            self.external_last_update_end = self.template_id.external_last_update_end
            self.model = self.template_id.model
            self.method = self.template_id.method
            self.external_model = self.template_id.external_model

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
                        'inclusion': object_field.inclusion,
                        'update': object_field.update,
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

    @api.multi
    @api.depends('schedule_ids')
    def _compute_count_schedules(self):
        for r in self:
            r.count_schedules = len(r.schedule_ids)

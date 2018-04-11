# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

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
        required=True,
        help="Model name of the object on which the synchronization method to be called is located, e.g. 'res.partner'"
    )

    method = fields.Char(
        string='Method',
        required=True,
        help="Name of the method to be called when the synchronization job is processed."
    )

    external_model = fields.Char(
        string='External Model',
        required=True,
        help="External model name, e.g. 'res.partner'"
    )

    external_sync_log = fields.Text(
        string="Synchronization Log"
    )

    active = fields.Boolean(string='Active', default=1)

    # _sql_constraints = [
    #     ('name_uniq',
    #      'UNIQUE (name)',
    #      u'Error! The Name must be unique!'),
    # ]

    @api.onchange('template_id')
    def onchange_template_id(self):
        if self.template_id:
            self.external_host_id = self.template_id.external_host_id
            self.external_exec_sync = self.template_id.external_exec_sync
            self.external_max_sync = self.template_id.external_max_sync
            self.external_last_update_start = self.template_id.external_last_update_start
            self.external_last_update_end = self.template_id.external_last_update_end
            self.model = self.template_id.model
            self.method = self.template_id.method
            self.external_model = self.template_id.external_model


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

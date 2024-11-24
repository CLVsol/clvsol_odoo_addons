# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSyncScheduleExec(models.TransientModel):
    _description = 'External Sync Schedule Exec'
    _name = 'clv.external_sync.schedule.exec'

    def _default_schedule_ids(self):
        return self._context.get('active_ids')
    schedule_ids = fields.Many2many(
        comodel_name='clv.external_sync.schedule',
        relation='clv_external_sync_schedule_exec_rel',
        string='Schedules to Execute',
        default=_default_schedule_ids)
    count_schedules = fields.Integer(
        string='Number of Schedules',
        compute='_compute_count_schedules',
        store=False
    )

    @api.depends('schedule_ids')
    def _compute_count_schedules(self):
        for r in self:
            r.count_schedules = len(r.schedule_ids)

    def do_external_sync_schedule_exec(self):
        self.ensure_one()

        for schedule in self.schedule_ids:

            model = schedule.model
            external_model = schedule.external_model
            _logger.info(u'%s %s [%s - %s]', '>>>>>', schedule.name, model, external_model)

            method_call = 'self.env["clv.external_sync"].' + schedule.method + '(schedule)'

            _logger.info(u'%s %s', '>>>>>>>>>>', method_call)

            if method_call:

                schedule.sync_log = 'method: ' + str(schedule.method) + '\n\n'
                schedule.sync_log +=  \
                    'external_host: ' + str(schedule.external_host_id.name) + '\n' + \
                    'external_dbname: ' + str(schedule.external_host_id.external_dbname) + '\n\n' + \
                    'max_task: ' + str(schedule.max_task) + '\n' + \
                    'enable_identification: ' + str(schedule.enable_identification) + '\n' + \
                    'enable_check_missing: ' + str(schedule.enable_check_missing) + '\n' + \
                    'enable_inclusion: ' + str(schedule.enable_inclusion) + '\n' + \
                    'enable_sync: ' + str(schedule.enable_sync) + '\n' + \
                    'external_last_update_args: ' + str(schedule.external_last_update_args()) + '\n\n' + \
                    'enable_sequence_code_sync: ' + str(schedule.enable_sequence_code_sync) + '\n\n'

                exec(method_call)

        return True

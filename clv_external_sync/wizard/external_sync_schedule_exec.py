# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSyncScheduleExec(models.TransientModel):
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

    @api.multi
    @api.depends('schedule_ids')
    def _compute_count_schedules(self):
        for r in self:
            r.count_schedules = len(r.schedule_ids)

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_external_sync_schedule_exec(self):
        self.ensure_one()

        for schedule in self.schedule_ids:

            _logger.info(u'%s %s', '>>>>>', schedule.name)

            method_call = 'self.env[schedule.model].' + schedule.method + '(schedule)'
            _logger.info(u'%s %s', '>>>>>>>>>>', method_call)

            exec(method_call)

        return True
        # return self._reopen_form()

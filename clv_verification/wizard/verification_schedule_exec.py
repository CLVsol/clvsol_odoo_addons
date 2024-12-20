# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class VerificationScheduleExec(models.TransientModel):
    _description = 'Verification Schedule Exec'
    _name = 'clv.verification.schedule.exec'

    def _default_schedule_ids(self):
        return self._context.get('active_ids')
    schedule_ids = fields.Many2many(
        comodel_name='clv.verification.schedule',
        relation='clv_verification_schedule_exec_rel',
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

    def do_verification_schedule_exec(self):
        self.ensure_one()

        from time import time
        start = time()

        for schedule in self.schedule_ids:

            _logger.info(u'%s %s [%s]', '>>>>>', schedule.name, schedule.model)

            items = False
            if (schedule.verify_all_items is False) and \
               (schedule.verification_set_elements is False) and \
               (schedule.model_items is not False):
                items = eval('schedule.' + schedule.model_items)
            elif (schedule.verify_all_items is False) and \
                 (schedule.verification_set_elements is True) and \
                 (schedule.verification_set_id is not False):
                set_elements = schedule.verification_set_id.set_element_ids
                items = []
                for set_element in set_elements:
                    items.append(set_element.ref_id)
            elif schedule.verify_all_items is True:
                Model = schedule.env[schedule.model]
                items = Model.search(eval(schedule.verification_domain_filter))

            _logger.info(u'%s %s %s', '>>>>>>>>>>', items, schedule.method)

            if len(items) > 0:

                method_call = False
                if schedule.method is not False:
                    # method_call = 'self.env["clv.verification.outcome"].' + schedule.method + '(schedule)'
                    method_call = 'items.' + schedule.method + '()'
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', schedule.method, method_call)

                if method_call:

                    schedule.verification_log = 'method: ' + str(schedule.method) + '\n\n'
                    schedule.verification_log +=  \
                        'items: ' + str(len(items)) + '\n\n'

                    exec(method_call)

            schedule.verification_log +=  \
                '\nExecution time: ' + str(secondsToStr(time() - start)) + '\n'

        return True

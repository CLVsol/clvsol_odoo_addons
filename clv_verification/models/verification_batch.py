# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class VerificationBatch(models.Model):
    _description = 'Verification Batch'
    _name = 'clv.verification.batch'
    _order = 'name'

    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s]' % (record.name, record.code)
                 ))
        return result

    name = fields.Char(string='Verification Batch Name', required=True, help="Verification Batch Name")

    code = fields.Char(string='Verification Batch Code', required=False)

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    verification_log = fields.Text(
        string="Synchronization Log"
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    @api.model
    def _verification_batch_exec(self, batch_name):

        from time import time
        start_total = time()

        VerificationBatch = self.env['clv.verification.batch']
        batch = VerificationBatch.search([
            ('name', '=', batch_name),
        ])

        verification_log = False

        _logger.info(u'%s %s', '>>>>>', batch.name)

        if verification_log is False:
            verification_log = '########## ' + batch.name + ' ##########\n'
        else:
            verification_log += '\n########## ' + batch.name + ' ##########\n'

        for verification_batch_member in batch.verification_batch_member_ids:

            if verification_batch_member.enabled:

                start = time()

                schedule = verification_batch_member.ref_id

                _logger.info(u'%s %s', '>>>>>', schedule.name)

                model = schedule.model
                _logger.info(u'%s %s [%s]', '>>>>>', schedule.name, model)

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
                        method_call = 'items.' + schedule.method + '()'
                        _logger.info(u'%s %s %s', '>>>>>>>>>>', schedule.method, method_call)

                    if method_call:

                        schedule.verification_log = 'method: ' + str(schedule.method) + '\n\n'
                        schedule.verification_log +=  \
                            'items: ' + str(len(items)) + '\n\n'

                        exec(method_call)

                        schedule.verification_log +=  \
                            '\nExecution time: ' + str(secondsToStr(time() - start)) + '\n'

                        verification_log += '\n########## ' + schedule.name + ' ##########\n'
                        verification_log += schedule.verification_log

                        self.env.cr.commit()

            verification_log += '\n############################################################'
            verification_log +=  \
                '\nExecution time: ' + str(secondsToStr(time() - start_total)) + '\n'

            batch.verification_log = verification_log

            _logger.info(u'%s %s', '>>>>> Execution time: ', secondsToStr(time() - start_total))

    @api.model
    def _verification_batch_exec_cron(self, batch_name):

        VerificationBatch = self.env['clv.verification.batch']
        VerificationBatch._verification_batch_exec(batch_name)

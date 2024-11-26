# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSyncBatch(models.Model):
    _description = 'External Sync Batch'
    _name = 'clv.external_sync.batch'
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

    name = fields.Char(string='External Sync Batch Name', required=True, help="External Sync Batch Name")

    code = fields.Char(string='External Sync Batch Code', required=False)

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    sync_log = fields.Text(
        string="Synchronization Log"
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    @api.model
    def _external_sync_batch_exec(self, batch_name):

        from time import time
        start = time()

        ExternalSyncBatch = self.env['clv.external_sync.batch']
        batch = ExternalSyncBatch.search([
            ('name', '=', batch_name),
        ])

        sync_log = False

        _logger.info(u'%s %s', '>>>>>', batch.name)

        if sync_log is False:
            sync_log = '########## ' + batch.name + ' ##########\n'
        else:
            sync_log += '\n########## ' + batch.name + ' ##########\n'

        for external_sync_batch_member in batch.external_sync_batch_member_ids:

            if external_sync_batch_member.enabled:

                schedule = external_sync_batch_member.ref_id

                _logger.info(u'%s %s', '>>>>>', schedule.name)

                model = schedule.model
                _logger.info(u'%s %s [%s]', '>>>>>', schedule.name, model)

                method_call = 'self.env["clv.external_sync"].' + schedule.method + '(schedule)'

                _logger.info(u'%s %s %s', '>>>>>>>>>>', schedule.method, method_call)

                if method_call:

                    schedule.sync_log = 'method: ' + str(schedule.method) + '\n\n'
                    schedule.sync_log +=  \
                        'external_host: ' + str(schedule.external_host_id.name) + '\n' + \
                        'external_dbname: ' + str(schedule.external_host_id.external_dbname) + '\n\n' + \
                        'max_task: ' + str(schedule.max_task) + '\n' + \
                        'enable_identification: ' + \
                        str(schedule.enable_identification) + '\n' + \
                        'enable_check_missing: ' + \
                        str(schedule.enable_check_missing) + '\n' + \
                        'enable_inclusion: ' + str(schedule.enable_inclusion) + '\n' + \
                        'enable_sync: ' + str(schedule.enable_sync) + '\n' + \
                        'external_last_update_args: ' + str(schedule.external_last_update_args()) + '\n\n' + \
                        'enable_sequence_code_sync: ' + str(schedule.enable_sequence_code_sync) + '\n\n'

                    exec(method_call)

                sync_log += '\n########## ' + schedule.name + ' ##########\n'
                sync_log += schedule.sync_log

                self.env.cr.commit()

        sync_log += '\n############################################################'
        sync_log +=  \
            '\nExecution time: ' + str(secondsToStr(time() - start)) + '\n'

        batch.sync_log = sync_log

        _logger.info(u'%s %s', '>>>>> Execution time: ', secondsToStr(time() - start))

    @api.model
    def _external_sync_batch_exec_cron(self, batch_name):

        ExternalSyncBatch = self.env['clv.external_sync.batch']
        ExternalSyncBatch._external_sync_batch_exec(batch_name)

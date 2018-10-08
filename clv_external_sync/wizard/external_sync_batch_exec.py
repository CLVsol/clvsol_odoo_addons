# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSyncBatchExec(models.TransientModel):
    _name = 'clv.external_sync.batch.exec'

    def _default_batch_ids(self):
        return self._context.get('active_ids')
    batch_ids = fields.Many2many(
        comodel_name='clv.external_sync.batch',
        relation='clv_external_sync_batch_exec_rel',
        string='Batchs to Execute',
        default=_default_batch_ids)
    count_batches = fields.Integer(
        string='Number of Batchs',
        compute='_compute_count_batches',
        store=False
    )

    @api.multi
    @api.depends('batch_ids')
    def _compute_count_batches(self):
        for r in self:
            r.count_batches = len(r.batch_ids)

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
    def do_external_sync_batch_exec(self):
        self.ensure_one()

        external_sync_log = False

        for batch in self.batch_ids:

            _logger.info(u'%s %s', '>>>>>', batch.name)

            if external_sync_log is False:
                external_sync_log = '########## ' + batch.name + ' ##########\n'
            else:
                external_sync_log += '\n########## ' + batch.name + ' ##########\n'

            for external_sync_batch_member in batch.external_sync_batch_member_ids:

                schedule = external_sync_batch_member.ref_id

                _logger.info(u'%s %s', '>>>>>', schedule.name)

                method_call = 'self.env[schedule.model].' + schedule.method + '(schedule)'
                _logger.info(u'%s %s', '>>>>>>>>>>', method_call)

                exec(method_call)

                external_sync_log += '\n########## ' + schedule.name + ' ##########\n'
                external_sync_log += schedule.external_sync_log

            batch.external_sync_log = external_sync_log

        return True
        # return self._reopen_form()

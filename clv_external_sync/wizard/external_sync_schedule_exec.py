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

            _logger.info(u'%s %s', '>>>>>>>>>>', schedule.name)

            from time import time
            start = time()

            external_host = schedule.external_host_id.name
            external_dbname = schedule.external_host_id.external_dbname
            external_user = schedule.external_host_id.external_user
            external_user_pw = schedule.external_host_id.external_user_pw

            ExternalSyncModel = self.env['clv.external_sync.model']
            uid, sock, login_msg = ExternalSyncModel.external_sync_host_login(
                external_host,
                external_dbname,
                external_user,
                external_user_pw
            )
            schedule.external_sync_log = 'login_msg: ' + str(login_msg) + '\n\n'

            Object = self.env[schedule.model]

            if uid is not False:

                external_object_fields = sock.execute(external_dbname, uid, external_user_pw,
                                                      schedule.external_model, 'fields_get',
                                                      [], {'attributes': ['string', 'help', 'type']})
                _logger.info(u'%s %s', '>>>>>>>>>>', external_object_fields.keys())

                args = []
                if schedule.external_last_update_start is not False and \
                   schedule.external_last_update_end is False:
                    args = [('write_date', '>=', schedule.external_last_update_start), ]
                if schedule.external_last_update_start is False and \
                   schedule.external_last_update_end is not False:
                    args += [('write_date', '<=', schedule.external_last_update_end), ]
                if schedule.external_last_update_start is not False and \
                   schedule.external_last_update_end is not False:
                    args += [('write_date', '>=', schedule.external_last_update_start),
                             ('write_date', '<=', schedule.external_last_update_end), ]
                _logger.info(u'%s %s', '>>>>>>>>>>', args)
                # external_object_ids = sock.execute(external_dbname, uid, external_user_pw,
                #                            schedule.external_model, 'search', args)
                # _logger.info(u'%s %s', '>>>>>>>>>>', len(external_object_ids))

                external_object_fields = ['name', 'code', '__last_update', ]
                # external_objects = sock.execute(external_dbname, uid, external_user_pw,
                #                         schedule.external_model, 'read',
                #                         external_object_ids,
                #                         external_object_fields)
                external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                                schedule.external_model, 'search_read',
                                                args,
                                                external_object_fields)

                _logger.info(u'%s %s', '>>>>>>>>>>', len(external_objects))

                reg_count = 0
                include_count = 0
                update_count = 0
                sync_count = 0
                sync_include_count = 0
                sync_update_count = 0
                for external_object in external_objects:

                    reg_count += 1

                    _logger.info(u'%s %s %s %s %s %s', '>>>>>>>>>>', reg_count,
                                 external_object['id'], external_object['name'], external_object['code'],
                                 external_object['__last_update'], )

                    local_object = Object.search([
                        ('code', '=', external_object['code']),
                    ])
                    if local_object.id is False:

                        include_count += 1

                        values = {
                            'name': external_object['name'],
                            'code': external_object['code'],
                            'external_id': external_object['id'],
                            'external_last_update': external_object['__last_update'],
                            'external_sync': 'included',
                        }
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, values)
                        new_local_object = Object.create(values)
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, new_local_object)

                        if schedule.external_exec_sync is True and \
                           sync_count < schedule.external_max_sync:

                            sync_count += 1
                            sync_include_count += 1

                            _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, new_local_object)

                            new_local_object.external_sync = 'synchronized'

                    else:

                        if external_object['__last_update'] > local_object.external_last_update and \
                           local_object.external_sync != 'included':

                            update_count += 1

                            local_object.external_sync = 'updated'

                        if local_object.external_sync != 'synchronized' and \
                           schedule.external_exec_sync is True and \
                           sync_count < schedule.external_max_sync:

                            sync_count += 1

                            _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, local_object)

                            if local_object.external_sync == 'included':

                                sync_include_count += 1

                                local_object.external_last_update = external_object['__last_update']
                                local_object.external_sync = 'synchronized'

                            if local_object.external_sync == 'updated':

                                sync_update_count += 1

                                local_object.external_last_update = external_object['__last_update']
                                local_object.external_sync = 'synchronized'

                _logger.info(u'%s %s', '>>>>>>>>>> external_exec_sync: ', schedule.external_exec_sync)
                _logger.info(u'%s %s', '>>>>>>>>>> external_max_sync: ', schedule.external_max_sync)
                _logger.info(u'%s %s', '>>>>>>>>>> args: ', args)
                _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
                _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
                _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
                _logger.info(u'%s %s', '>>>>>>>>>> sync_include_count: ', sync_include_count)
                _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count: ', sync_update_count)
                _logger.info(u'%s %s', '>>>>>>>>>> sync_count: ', sync_count)
                _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

                schedule.external_sync_log += 'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n'
                schedule.external_sync_log += 'external_max_sync: ' + str(schedule.external_max_sync) + '\n'
                schedule.external_sync_log += 'args: ' + str(args) + '\n\n'
                schedule.external_sync_log += 'reg_count: ' + str(reg_count) + '\n'
                schedule.external_sync_log += 'include_count: ' + str(include_count) + '\n'
                schedule.external_sync_log += 'update_count: ' + str(update_count) + '\n'
                schedule.external_sync_log += 'sync_include_count: ' + str(sync_include_count) + '\n'
                schedule.external_sync_log += 'sync_update_count: ' + str(sync_update_count) + '\n'
                schedule.external_sync_log += 'sync_count: ' + str(sync_count) + '\n\n'

            schedule.external_sync_log += 'Execution time: ' + str(secondsToStr(time() - start)) + '\n'

        return True
        # return self._reopen_form()

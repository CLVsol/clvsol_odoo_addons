# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime
from functools import reduce
from ast import literal_eval

from odoo import models

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSync(models.Model):
    _inherit = 'clv.external_sync'

    def _res_users_migration(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            remote_object_fields = ['id', 'name', 'partner_id', 'company_id', 'tz', 'lang',
                                    'login', 'password', 'image_1920', 'groups_id', 'active']

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            ResUsers = self.env['res.users']
            ResCompany = self.env['res.company']
            ResPartner = self.env['res.partner']

            external_host = schedule.external_host_id.name
            external_dbname = schedule.external_host_id.external_dbname
            external_user = schedule.external_host_id.external_user
            external_user_pw = schedule.external_host_id.external_user_pw

            uid, sock, login_msg = AbstractExternalSync.external_sync_host_login(
                external_host,
                external_dbname,
                external_user,
                external_user_pw
            )
            schedule.sync_log += 'login_msg: ' + str(login_msg) + '\n\n'

            object_count = 0

            if uid is not False:

                schedule.sync_log += 'Executing: "' + '_res_users_migration' + '"...\n\n'

                remote_objects = sock.execute(external_dbname, uid, external_user_pw,
                                              'res.users', 'search_read',
                                              [],
                                              remote_object_fields)

                _logger.info(u'%s %s\n', '--> remote_objects', len(remote_objects))

                for remote_object in remote_objects:

                    object_count += 1

                    _logger.info(u'%s %s %s', '-->', object_count, remote_object['name'])

                    local_object = ResUsers.search([('login', '=', remote_object['login'])])

                    if local_object.id is not False:
                        _logger.info(u'%s %s', '----->', '*** Skipped ***')

                    else:

                        company = ResCompany.search([('name', 'in', remote_object['company_id'])])
                        parent = ResPartner.search([('name', 'in', remote_object['company_id'])])

                        res_user_record = {}
                        res_user_record['name'] = remote_object['name']
                        res_user_record['login'] = remote_object['login']
                        res_user_record['password'] = remote_object['password']
                        if remote_object['image_1920'] is not False:
                            res_user_record['image_1920'] = remote_object['image_1920']
                        res_user_record['lang'] = remote_object['lang']
                        res_user_record['tz'] = remote_object['tz']
                        res_user_record['active'] = remote_object['active']
                        new_user = ResUsers.create(res_user_record)

                        _logger.info(u'%s %s', '----->', new_user)

                        new_partner = ResPartner.search([('id', '=', new_user.partner_id.id)])

                        _logger.info(u'%s %s', '----->', new_partner)

                        res_partner_record = {}
                        res_partner_record['email'] = remote_object['login']
                        res_partner_record['parent_id'] = parent.id
                        res_partner_record['company_id'] = company.id
                        new_partner.write(res_partner_record)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import ssl
import xmlrpc
from datetime import datetime
from functools import reduce

from odoo import api, models, fields

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class AbstractExternalSync(models.AbstractModel):
    _name = 'clv.abstract.external_sync'

    external_id = fields.Integer(string='External ID')
    external_last_update = fields.Datetime(string="External Last Update")
    external_sync = fields.Selection(
        [('included', 'Included'),
         ('updated', 'Updated'),
         ('synchronized', 'Synchronized'),
         ('missing', 'Missing'),
         ], 'External Synchronization'
    )

    @api.model
    def external_sync_host_login(self, external_host, external_dbname, external_user, external_user_pw):

        uid = False
        sock = False

        xmlrpc_sock_common_url = external_host + '/xmlrpc/2/common'
        xmlrpc_sock_str = external_host + '/xmlrpc/2/object'

        server_version = False

        login_msg = ''
        user_name = ''
        company_name = ''

        # ctx = ssl.SSLContext()
        ssl._create_default_https_context = ssl._create_unverified_context
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock_common = xmlrpc.client.ServerProxy(xmlrpc_sock_common_url, context=ctx)
        try:
            server_version = sock_common.version()
        except Exception:
            pass

        if server_version is not False:
            pass
        else:
            login_msg = '[11] Server is not responding.'
            _logger.info(u'%s %s %s %s', '>>>>>',
                         login_msg,
                         user_name,
                         company_name)
            return uid, sock, login_msg

        try:
            sock_common = xmlrpc.client.ServerProxy(xmlrpc_sock_common_url)
            uid = sock_common.login(external_dbname, external_user, external_user_pw)
            sock = xmlrpc.client.ServerProxy(xmlrpc_sock_str)
            _logger.info(u'%s %s', '>>>>>>>>>> sock', sock)
        except Exception as e:
            _logger.info(u'%s %s %s %s', '>>>>>', e)
            pass

        if uid is not False:
            pass
        else:
            login_msg = '[21] Invalid Login/Pasword.'
            _logger.info(u'%s %s %s %s', '>>>>>',
                         login_msg,
                         user_name,
                         company_name)
            return uid, sock, login_msg

        try:
            sock_common = xmlrpc.client.ServerProxy(xmlrpc_sock_common_url)
            uid = sock_common.login(external_dbname, external_user, external_user_pw)
            sock = xmlrpc.client.ServerProxy(xmlrpc_sock_str)
        except Exception:
            pass

        user_fields = ['name', 'parent_id', ]
        user_data = sock.execute(external_dbname, uid, external_user_pw, 'res.users', 'read',
                                 uid, user_fields)[0]
        user_name = user_data['name']
        parent_id = user_data['parent_id']

        if parent_id is not False:
            args = [('id', '=', parent_id[0])]
            company_id = sock.execute(external_dbname, uid, external_user_pw, 'res.company', 'search', args)

            company_fields = ['name', ]
            company_data = sock.execute(external_dbname, uid, external_user_pw, 'res.company', 'read',
                                        company_id[0], company_fields)[0]
            company_name = company_data['name']

        if uid is not False:
            login_msg = '[01] Login Ok.'
            _logger.info(u'%s %s %s %s', '>>>>>',
                         login_msg,
                         user_name,
                         company_name)

        if uid is not False:

            user_fields = ['name', 'parent_id', ]
            user_data = sock.execute(external_dbname, uid, external_user_pw, 'res.users', 'read',
                                     uid, user_fields)[0]
            user_name = user_data['name']
            parent_id = user_data['parent_id'][0]

            _logger.info(u'%s %s', '>>>>>>>>>>', user_data)

        return uid, sock, login_msg

    def _object_synchronize(
        self, sock, external_dbname, uid, external_user_pw,
        external_model, external_id, schedule
    ):

        external_object_fields = []
        local_object_fields = []
        for object_field in schedule.object_field_ids:
            if object_field.update is True:
                external_object_fields.append(object_field.external_object_field)
                local_object_fields.append(object_field.local_object_field)
        external_object_fields.append('__last_update')
        local_object_fields.append('external_last_update')
        args = [('id', '=', external_id)]
        external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                        external_model, 'search_read',
                                        args,
                                        external_object_fields)

        external_object = external_objects[0]

        _logger.info(u'>>>>>>>>>>>>>>> %s %s', external_object, self)

        i = 0
        values = {}
        for field in local_object_fields:
            values[local_object_fields[i]] = external_object[external_object_fields[i]]
            i += 1
        values['external_sync'] = 'synchronized'

        self.write(values)

    def _object_external_sync(self, schedule):

        from time import time
        start = time()

        date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        upmost_last_update = False

        external_host = schedule.external_host_id.name
        external_dbname = schedule.external_host_id.external_dbname
        external_user = schedule.external_host_id.external_user
        external_user_pw = schedule.external_host_id.external_user_pw

        AbstractExternalSync = self.env['clv.abstract.external_sync']
        uid, sock, login_msg = AbstractExternalSync.external_sync_host_login(
            external_host,
            external_dbname,
            external_user,
            external_user_pw
        )
        schedule.external_sync_log = 'login_msg: ' + str(login_msg) + '\n\n'

        if uid is not False:

            Object = self.env[schedule.model]

            external_object_ids = sock.execute(external_dbname, uid, external_user_pw,
                                               schedule.external_model, 'search', [])
            _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_object_ids))

            local_objects = Object.search([
                ('external_id', '!=', False),
                ('external_sync', '!=', 'missing'),
            ])
            _logger.info(u'%s %s', '>>>>>>>>>> (local_objects):', len(local_objects))

            missing_count = 0
            for local_object in local_objects:
                if local_object.external_id not in external_object_ids:
                    missing_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>> (missing_object):', missing_count, local_object.id)
                    local_object.external_sync = 'missing'

            external_object_fields = sock.execute(external_dbname, uid, external_user_pw,
                                                  schedule.external_model, 'fields_get',
                                                  [], {'attributes': ['string', 'help', 'type']})
            _logger.info(u'%s %s', '>>>>>>>>>> (external_object_fields):', external_object_fields.keys())

            args = schedule.external_last_update_args()
            _logger.info(u'%s %s', '>>>>>>>>>> (args):', args)

            external_object_fields = []
            local_object_fields = []
            for object_field in schedule.object_field_ids:
                if object_field.inclusion is True:
                    external_object_fields.append(object_field.external_object_field)
                    local_object_fields.append(object_field.local_object_field)
            external_object_fields.append('__last_update')
            local_object_fields.append('external_last_update')
            _logger.info(u'%s %s %s', '>>>>>>>>>> (external_object_fields):',
                         external_object_fields,
                         local_object_fields)
            external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                            schedule.external_model, 'search_read',
                                            args,
                                            external_object_fields)

            _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_objects))

            reg_count = 0
            include_count = 0
            update_count = 0
            sync_count = 0
            sync_include_count = 0
            sync_update_count = 0
            for external_object in external_objects:

                reg_count += 1

                _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count,
                             external_object['id'],
                             external_object['__last_update'], )

                if upmost_last_update is False:
                    upmost_last_update = external_object['__last_update']
                else:
                    if external_object['__last_update'] > upmost_last_update:
                        upmost_last_update = external_object['__last_update']

                local_object = Object.search([
                    ('external_id', '=', external_object['id']),
                ])

                if local_object.id is False:

                    include_count += 1

                    i = 0
                    values = {}
                    for field in local_object_fields:
                        values[local_object_fields[i]] = external_object[external_object_fields[i]]
                        i += 1
                    values['external_id'] = external_object['id']
                    values['external_sync'] = 'included'

                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, values)
                    new_local_object = Object.create(values)
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, new_local_object)

                    if schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        sync_count += 1
                        sync_include_count += 1

                        new_local_object._object_synchronize(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['id'],
                            schedule
                        )

                else:

                    if external_object['__last_update'] > local_object.external_last_update and \
                       local_object.external_sync != 'included':

                        update_count += 1

                        local_object.external_sync = 'updated'

                    if (local_object.external_sync == 'included' or
                        local_object.external_sync == 'updated') and \
                       schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        sync_count += 1

                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, local_object)

                        if local_object.external_sync == 'included':
                            sync_include_count += 1

                        if local_object.external_sync == 'updated':
                            sync_update_count += 1

                        local_object._object_synchronize(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['id'],
                            schedule
                        )

            local_objects = Object.search([
                ('external_sync', '=', 'updated'),
            ])
            _logger.info(u'>>>>>>>>>>>>>>> (local_objects): %s %s', local_objects, len(local_objects))

            reg_count_2 = 0
            sync_update_count_2 = 0
            while len(local_objects) > 0 and \
                    sync_count < schedule.external_max_sync:

                for external_object in external_objects:

                    reg_count_2 += 1

                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count_2,
                                 external_object['id'],
                                 external_object['__last_update'], )

                    if upmost_last_update is False:
                        upmost_last_update = external_object['__last_update']
                    else:
                        if external_object['__last_update'] > upmost_last_update:
                            upmost_last_update = external_object['__last_update']

                    local_object = Object.search([
                        ('external_id', '=', external_object['id']),
                    ])

                    if local_object.external_sync == 'updated' and \
                       schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, local_object)

                        if local_object.external_sync == 'updated':
                            sync_update_count_2 += 1

                        local_object._object_synchronize(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['id'],
                            schedule
                        )

                local_objects = Object.search([
                    ('external_sync', '=', 'updated'),
                ])
                _logger.info(u'>>>>>>>>>>>>>>> (local_objects): %s %s', local_objects, len(local_objects))

            _logger.info(u'%s %s', '>>>>>>>>>> external_exec_sync: ', schedule.external_exec_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> external_max_sync: ', schedule.external_max_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> args: ', args)
            _logger.info(u'%s %s', '>>>>>>>>>> external_object_ids: ', len(external_object_ids))
            _logger.info(u'%s %s', '>>>>>>>>>> local_objects: ', len(local_objects))
            _logger.info(u'%s %s', '>>>>>>>>>> missing_count: ', missing_count)
            _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
            _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_include_count: ', sync_include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count: ', sync_update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_count: ', sync_count)
            _logger.info(u'%s %s', '>>>>>>>>>> reg_count_2: ', reg_count_2)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count_2: ', sync_update_count_2)
            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.upmost_last_update = upmost_last_update
            schedule.external_sync_log +=  \
                'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n' + \
                'external_max_sync: ' + str(schedule.external_max_sync) + '\n' + \
                'args: ' + str(args) + '\n\n' + \
                'external_object_ids: ' + str(len(external_object_ids)) + '\n' + \
                'local_objects: ' + str(len(local_objects)) + '\n' + \
                'missing_count: ' + str(missing_count) + '\n\n' + \
                'reg_count: ' + str(reg_count) + '\n' + \
                'include_count: ' + str(include_count) + '\n' + \
                'update_count: ' + str(update_count) + '\n' + \
                'sync_include_count: ' + str(sync_include_count) + '\n' + \
                'sync_update_count: ' + str(sync_update_count) + '\n' + \
                'sync_count: ' + str(sync_count) + '\n\n' + \
                'reg_count_2: ' + str(reg_count_2) + '\n' + \
                'sync_update_count_2: ' + str(sync_update_count_2) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n'

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
    _description = 'Abstract External Sync'
    _name = 'clv.abstract.external_sync'

    external_id = fields.Integer(string='External ID')
    external_last_update = fields.Datetime(string="External Last Update")
    external_sync = fields.Selection(
        [('included', 'Included'),
         ('updated', 'Updated'),
         ('synchronized', 'Synchronized'),
         ('recognized', 'Recognized'),
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
            _logger.info(u'%s %s', '>>>>> uid', uid)
            sock = xmlrpc.client.ServerProxy(xmlrpc_sock_str)
            _logger.info(u'%s %s', '>>>>> sock', sock)
        except Exception as e:
            _logger.info(u'%s %s', '>>>>> except', e)
            login_msg = '[22] Database does not exist.'
            _logger.info(u'%s %s %s %s', '>>>>>',
                         login_msg,
                         user_name,
                         company_name)
            return uid, sock, login_msg

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
            parent_id = False
            if user_data['parent_id'] is not False:
                parent_id = user_data['parent_id'][0]

            _logger.info(u'%s %s', '>>>>>>>>>>', user_data)

        return uid, sock, login_msg

    # def _object_synchronize(
    #     self, sock, external_dbname, uid, external_user_pw,
    #     external_model, external_id, schedule
    # ):

    #     Model = self.env['ir.model']
    #     ModelFields = self.env['ir.model.fields']

    #     local_object_model = Model.search([
    #         ('model', '=', self._name),
    #     ])

    #     external_object_fields = []
    #     local_object_fields = []
    #     for object_field in schedule.object_field_ids:
    #         if object_field.update is True:
    #             external_object_fields.append(object_field.external_object_field)
    #             local_object_fields.append(object_field.local_object_field)
    #     external_object_fields.append('__last_update')
    #     local_object_fields.append('external_last_update')

    #     external_args = [
    #         ('id', '=', external_id),
    #     ]
    #     if 'active' in external_object_fields:
    #         external_args = [
    #             ('id', '=', external_id),
    #             '|',
    #             ('active', '=', True),
    #             ('active', '=', False),
    #         ]

    #     external_objects = sock.execute(external_dbname, uid, external_user_pw,
    #                                     external_model, 'search_read',
    #                                     external_args,
    #                                     external_object_fields)

    #     external_object = external_objects[0]

    #     _logger.info(u'>>>>>>>>>>>>>>> %s %s', external_object, self)

    #     external_sync = 'synchronized'

    #     i = 0
    #     values = {}
    #     for field in local_object_fields:
    #         fields = ModelFields.search([
    #             ('model_id', '=', local_object_model.id),
    #             ('name', '=', local_object_fields[i]),
    #         ])

    #         if fields.id is not False:

    #             if fields[0].ttype in ['char', 'date', 'datetime', 'text', 'html', 'integer', 'boolean']:
    #                 values[local_object_fields[i]] = external_object[external_object_fields[i]]

    #             elif fields[0].ttype == 'many2one':
    #                 if external_object[external_object_fields[i]] is not False:
    #                     model_ = fields[0].relation
    #                     id_ = external_object[external_object_fields[i]][0]
    #                     RelationObject = self.env[model_]
    #                     try:
    #                         relation_object = RelationObject.with_context({'active_test': False}).search([
    #                             ('external_id', '=', int(id_)),
    #                         ])
    #                         if relation_object.id is not False:
    #                             values[local_object_fields[i]] = relation_object.id
    #                         else:
    #                             _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s (%s)',
    #                                             fields[0].name, fields[0].ttype, id_)
    #                             external_sync = 'updated'
    #                     except ValueError as e:
    #                         _logger.error(u'>>>>>>>>>>>>>>>>>>>> %s', e)
    #                         external_sync = 'updated'

    #             elif fields[0].ttype == 'reference':
    #                 if external_object[external_object_fields[i]] is not False:
    #                     model_, id_ = external_object[external_object_fields[i]].split(',')
    #                     RefObject = self.env[model_]
    #                     ref_object = RefObject.with_context({'active_test': False}).search([
    #                         ('external_id', '=', int(id_)),
    #                     ])
    #                     if ref_object.id is not False:
    #                         values[local_object_fields[i]] = model_ + ',' + str(ref_object.id)
    #                     else:
    #                         _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)
    #                         external_sync = 'updated'

    #             elif fields[0].ttype == 'many2many':
    #                 if external_object[external_object_fields[i]] is not False:
    #                     model_ = fields[0].relation
    #                     ids_ = external_object[external_object_fields[i]]
    #                     RelationObject = self.env[model_]

    #                     m2m_list = []
    #                     m2m_list.append((5,))
    #                     for external_id in ids_:
    #                         relation_object = RelationObject.with_context({'active_test': False}).search([
    #                             ('external_id', '=', external_id),
    #                         ])
    #                         if relation_object.id is not False:
    #                             m2m_list.append((4, relation_object.id))
    #                         else:
    #                             _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s (%s)',
    #                                             fields[0].name, fields[0].ttype, id_)
    #                             external_sync = 'updated'

    #                     _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
    #                     values[local_object_fields[i]] = m2m_list

    #             else:
    #                 _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)
    #                 external_sync = 'updated'

    #         else:
    #             _logger.error(u'>>>>>>>>>>>>>>>>>>>> %s %s', local_object_fields[i], fields)

    #         i += 1

    #     values['external_sync'] = external_sync

    #     self.write(values)

    def _object_synchronize_2(
        self, sock, external_dbname, uid, external_user_pw,
        external_model, external_id, schedule, model_name,
        sync_object
    ):

        Model = self.env['ir.model']
        ModelFields = self.env['ir.model.fields']
        ExternalSync = self.env['clv.external_sync']

        local_object_model = Model.search([
            ('model', '=', model_name),
        ])

        LocalObject = self.env[model_name]
        local_object = LocalObject.with_context({'active_test': False}).search([
            ('id', '=', self.res_id),
        ])

        external_object_fields = []
        local_object_fields = []
        for object_field in schedule.object_field_ids:
            if object_field.update is True:
                external_object_fields.append(object_field.external_object_field)
                local_object_fields.append(object_field.local_object_field)
        external_object_fields.append('__last_update')

        external_args = [
            ('id', '=', external_id),
        ]
        if 'active' in external_object_fields:
            external_args = [
                ('id', '=', external_id),
                '|',
                ('active', '=', True),
                ('active', '=', False),
            ]

        external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                        external_model, 'search_read',
                                        external_args,
                                        external_object_fields)

        external_object = external_objects[0]

        _logger.info(u'>>>>>>>>>>>>>>> %s %s', external_object, local_object)

        external_sync = 'synchronized'

        i = 0
        local_values = {}
        for field in local_object_fields:
            fields = ModelFields.search([
                ('model_id', '=', local_object_model.id),
                ('name', '=', local_object_fields[i]),
            ])

            if fields.id is not False:

                if fields[0].ttype in ['char', 'date', 'datetime', 'text', 'html', 'integer', 'boolean', 'selection']:
                    local_values[local_object_fields[i]] = external_object[external_object_fields[i]]

                elif fields[0].ttype == 'many2one':
                    if external_object[external_object_fields[i]] is not False:
                        model_ = fields[0].relation
                        id_ = external_object[external_object_fields[i]][0]
                        relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                            ('model', '=', model_),
                            ('external_id', '=', int(id_)),
                        ])
                        RelationObject = self.env[model_]
                        relation_object = RelationObject.with_context({'active_test': False}).search([
                            # ('external_id', '=', int(id_)),
                            ('id', '=', relation_sync_object.res_id),
                        ])
                        if relation_object.id is not False:
                            local_values[local_object_fields[i]] = relation_object.id
                        else:
                            _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s (%s)', fields[0].name, fields[0].ttype, id_)
                            # external_sync = 'updated'
                            external_sync = 'updated'

                elif fields[0].ttype == 'reference':
                    if external_object[external_object_fields[i]] is not False:
                        model_, id_ = external_object[external_object_fields[i]].split(',')
                        try:
                            relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                ('model', '=', model_),
                                ('external_id', '=', int(id_)),
                            ])
                            RefObject = self.env[model_]
                            ref_object = RefObject.with_context({'active_test': False}).search([
                                # ('external_id', '=', int(id_)),
                                ('id', '=', relation_sync_object.res_id),
                            ])
                            if ref_object.id is not False:
                                local_values[local_object_fields[i]] = model_ + ',' + str(ref_object.id)
                            else:
                                _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)
                                external_sync = 'updated'
                        except KeyError:
                            _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', model_, id_)
                            external_sync = 'updated'

                elif fields[0].ttype == 'many2many':
                    if external_object[external_object_fields[i]] is not False:
                        model_ = fields[0].relation
                        ids_ = external_object[external_object_fields[i]]
                        RelationObject = self.env[model_]

                        m2m_list = []
                        m2m_list.append((5,))
                        for external_id in ids_:
                            relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                ('model', '=', model_),
                                ('external_id', '=', int(external_id)),
                            ])
                            RelationObject = self.env[model_]
                            relation_object = RelationObject.with_context({'active_test': False}).search([
                                # ('external_id', '=', int(id_)),
                                ('id', '=', relation_sync_object.res_id),
                            ])
                            if relation_object.id is not False:
                                m2m_list.append((4, relation_object.id))
                            else:
                                _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s (%s)',
                                                fields[0].name, fields[0].ttype, id_)
                                external_sync = 'updated'

                        _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                        local_values[local_object_fields[i]] = m2m_list

                else:
                    _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)
                    external_sync = 'updated'

            else:
                _logger.error(u'>>>>>>>>>>>>>>>>>>>> %s %s', local_object_fields[i], fields)

            i += 1

        local_object.write(local_values)

        self.external_last_update = external_object['__last_update']
        self.external_sync = external_sync

    # def _object_external_sync(self, schedule):

    #     from time import time
    #     start = time()

    #     Model = self.env['ir.model']
    #     ModelFields = self.env['ir.model.fields']

    #     local_object_model = Model.search([
    #         ('model', '=', self._name),
    #     ])

    #     date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     upmost_last_update = False

    #     external_host = schedule.external_host_id.name
    #     external_dbname = schedule.external_host_id.external_dbname
    #     external_user = schedule.external_host_id.external_user
    #     external_user_pw = schedule.external_host_id.external_user_pw

    #     AbstractExternalSync = self.env['clv.abstract.external_sync']
    #     uid, sock, login_msg = AbstractExternalSync.external_sync_host_login(
    #         external_host,
    #         external_dbname,
    #         external_user,
    #         external_user_pw
    #     )
    #     schedule.external_sync_log = 'login_msg: ' + str(login_msg) + '\n\n'

    #     if uid is not False:

    #         Object = self.env[schedule.model]

    #         external_object_fields = []
    #         local_object_fields = []
    #         for object_field in schedule.object_field_ids:
    #             external_object_fields.append(object_field.external_object_field)

    #         external_search_args = []
    #         if 'active' in external_object_fields:
    #             external_search_args = [
    #                 '|',
    #                 ('active', '=', True),
    #                 ('active', '=', False),
    #             ]

    #         external_object_ids = sock.execute(external_dbname, uid, external_user_pw,
    #                                            schedule.external_model, 'search', external_search_args)
    #         _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_object_ids))

    #         local_objects = Object.with_context({'active_test': False}).search([
    #             ('external_id', '!=', False),
    #             ('external_sync', '!=', 'missing'),
    #         ])
    #         _logger.info(u'%s %s', '>>>>>>>>>> (local_objects):', len(local_objects))

    #         missing_count = 0
    #         for local_object in local_objects:
    #             if local_object.external_id not in external_object_ids:
    #                 missing_count += 1
    #                 _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>> (missing_object):', missing_count, local_object.id)
    #                 local_object.external_sync = 'missing'

    #         external_object_fields = sock.execute(external_dbname, uid, external_user_pw,
    #                                               schedule.external_model, 'fields_get',
    #                                               [], {'attributes': ['string', 'help', 'type']})
    #         _logger.info(u'%s %s', '>>>>>>>>>> (external_object_fields):', external_object_fields.keys())

    #         external_args = schedule.external_last_update_args() + external_search_args
    #         _logger.info(u'%s %s', '>>>>>>>>>> (external_args):', external_args)

    #         external_object_fields = []
    #         local_object_fields = []
    #         for object_field in schedule.object_field_ids:
    #             if object_field.inclusion is True:
    #                 external_object_fields.append(object_field.external_object_field)
    #                 local_object_fields.append(object_field.local_object_field)
    #         external_object_fields.append('__last_update')
    #         local_object_fields.append('external_last_update')
    #         _logger.info(u'%s %s %s', '>>>>>>>>>> (external_object_fields):',
    #                      external_object_fields,
    #                      local_object_fields)
    #         external_objects = sock.execute(external_dbname, uid, external_user_pw,
    #                                         schedule.external_model, 'search_read',
    #                                         external_args,
    #                                         external_object_fields)

    #         _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_objects))

    #         reg_count = 0
    #         include_count = 0
    #         update_count = 0
    #         sync_count = 0
    #         sync_include_count = 0
    #         sync_update_count = 0
    #         for external_object in external_objects:

    #             reg_count += 1

    #             _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count,
    #                          external_object['id'],
    #                          external_object['__last_update'], )

    #             if upmost_last_update is False:
    #                 upmost_last_update = external_object['__last_update']
    #             else:
    #                 if external_object['__last_update'] > upmost_last_update:
    #                     upmost_last_update = external_object['__last_update']

    #             local_object = Object.with_context({'active_test': False}).search([
    #                 ('external_id', '=', external_object['id']),
    #             ])

    #             if local_object.id is False:

    #                 include_count += 1

    #                 i = 0
    #                 values = {}
    #                 for field in local_object_fields:
    #                     fields = ModelFields.search([
    #                         ('model_id', '=', local_object_model.id),
    #                         ('name', '=', local_object_fields[i]),
    #                     ])

    #                     if fields[0].ttype in ['char', 'date', 'datetime', 'text', 'integer', 'boolean']:
    #                         values[local_object_fields[i]] = external_object[external_object_fields[i]]

    #                     elif fields[0].ttype == 'many2one':
    #                         if external_object[external_object_fields[i]] is not False:
    #                             model_ = fields[0].relation
    #                             id_ = external_object[external_object_fields[i]][0]
    #                             RelationObject = self.env[model_]
    #                             relation_object = RelationObject.with_context({'active_test': False}).search([
    #                                 ('external_id', '=', int(id_)),
    #                             ])
    #                             if relation_object.id is not False:
    #                                 values[local_object_fields[i]] = relation_object.id

    #                     elif fields[0].ttype == 'reference':
    #                         if external_object[external_object_fields[i]] is not False:
    #                             model_, id_ = external_object[external_object_fields[i]].split(',')
    #                             RefObject = self.env[model_]
    #                             ref_object = RefObject.with_context({'active_test': False}).search([
    #                                 ('external_id', '=', int(id_)),
    #                             ])
    #                             if ref_object.id is not False:
    #                                 values[local_object_fields[i]] = model_ + ',' + str(ref_object.id)

    #                     elif fields[0].ttype == 'many2many':
    #                         if external_object[external_object_fields[i]] is not False:
    #                             model_ = fields[0].relation
    #                             ids_ = external_object[external_object_fields[i]]
    #                             RelationObject = self.env[model_]

    #                             m2m_list = []
    #                             m2m_list.append((5,))
    #                             for external_id in ids_:
    #                                 relation_object = RelationObject.with_context({'active_test': False}).search([
    #                                     ('external_id', '=', external_id),
    #                                 ])
    #                                 if relation_object.id is not False:
    #                                     m2m_list.append((4, relation_object.id))

    #                             _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
    #                             values[local_object_fields[i]] = m2m_list

    #                     else:
    #                         _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)

    #                     i += 1
    #                     # values[local_object_fields[i]] = external_object[external_object_fields[i]]
    #                     # i += 1
    #                 values['external_id'] = external_object['id']
    #                 values['external_sync'] = 'included'

    #                 _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, values)
    #                 new_local_object = Object.create(values)

    #                 if schedule.external_exec_sync is True and \
    #                    sync_count < schedule.external_max_sync:

    #                     sync_count += 1
    #                     sync_include_count += 1

    #                     new_local_object._object_synchronize(
    #                         sock, external_dbname, uid, external_user_pw,
    #                         schedule.external_model, external_object['id'],
    #                         schedule
    #                     )

    #             else:

    #                 if external_object['__last_update'] > local_object.external_last_update and \
    #                    local_object.external_sync != 'included':

    #                     update_count += 1

    #                     local_object.external_sync = 'updated'

    #                 if (local_object.external_sync == 'included' or
    #                     local_object.external_sync == 'updated') and \
    #                    schedule.external_exec_sync is True and \
    #                    sync_count < schedule.external_max_sync:

    #                     sync_count += 1

    #                     _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, local_object)

    #                     if local_object.external_sync == 'included':
    #                         sync_include_count += 1

    #                     if local_object.external_sync == 'updated':
    #                         sync_update_count += 1

    #                     local_object._object_synchronize(
    #                         sock, external_dbname, uid, external_user_pw,
    #                         schedule.external_model, external_object['id'],
    #                         schedule
    #                     )

    #         local_objects = Object.with_context({'active_test': False}).search([
    #             ('external_sync', '=', 'updated'),
    #         ])
    #         _logger.info(u'>>>>>>>>>>>>>>> (local_objects): %s %s', local_objects, len(local_objects))

    #         reg_count_2 = 0
    #         sync_update_count_2 = 0
    #         while len(local_objects) > 0 and \
    #                 sync_count < schedule.external_max_sync:

    #             for external_object in external_objects:

    #                 reg_count_2 += 1

    #                 _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count_2,
    #                              external_object['id'],
    #                              external_object['__last_update'], )

    #                 if upmost_last_update is False:
    #                     upmost_last_update = external_object['__last_update']
    #                 else:
    #                     if external_object['__last_update'] > upmost_last_update:
    #                         upmost_last_update = external_object['__last_update']

    #                 local_object = Object.with_context({'active_test': False}).search([
    #                     ('external_id', '=', external_object['id']),
    #                 ])

    #                 if local_object.external_sync == 'updated' and \
    #                    schedule.external_exec_sync is True and \
    #                    sync_count < schedule.external_max_sync:

    #                     sync_count += 1

    #                     _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, local_object)

    #                     if local_object.external_sync == 'updated':
    #                         sync_update_count_2 += 1

    #                     local_object._object_synchronize(
    #                         sock, external_dbname, uid, external_user_pw,
    #                         schedule.external_model, external_object['id'],
    #                         schedule
    #                     )

    #             local_objects = Object.with_context({'active_test': False}).search([
    #                 ('external_sync', '=', 'updated'),
    #             ])
    #             _logger.info(u'>>>>>>>>>>>>>>> (local_objects): %s %s', local_objects, len(local_objects))

    #         _logger.info(u'%s %s', '>>>>>>>>>> external_exec_sync: ', schedule.external_exec_sync)
    #         _logger.info(u'%s %s', '>>>>>>>>>> external_max_sync: ', schedule.external_max_sync)
    #         _logger.info(u'%s %s', '>>>>>>>>>> external_args: ', external_args)
    #         _logger.info(u'%s %s', '>>>>>>>>>> external_object_ids: ', len(external_object_ids))
    #         _logger.info(u'%s %s', '>>>>>>>>>> local_objects: ', len(local_objects))
    #         _logger.info(u'%s %s', '>>>>>>>>>> missing_count: ', missing_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> sync_include_count: ', sync_include_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count: ', sync_update_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> sync_count: ', sync_count)
    #         _logger.info(u'%s %s', '>>>>>>>>>> reg_count_2: ', reg_count_2)
    #         _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count_2: ', sync_update_count_2)
    #         _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
    #         _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
    #         _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

    #         schedule.date_last_sync = date_last_sync
    #         schedule.upmost_last_update = upmost_last_update
    #         schedule.external_sync_log +=  \
    #             'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n' + \
    #             'external_max_sync: ' + str(schedule.external_max_sync) + '\n' + \
    #             'external_args: ' + str(external_args) + '\n\n' + \
    #             'external_object_ids: ' + str(len(external_object_ids)) + '\n' + \
    #             'local_objects: ' + str(len(local_objects)) + '\n' + \
    #             'missing_count: ' + str(missing_count) + '\n\n' + \
    #             'reg_count: ' + str(reg_count) + '\n' + \
    #             'include_count: ' + str(include_count) + '\n' + \
    #             'update_count: ' + str(update_count) + '\n' + \
    #             'sync_include_count: ' + str(sync_include_count) + '\n' + \
    #             'sync_update_count: ' + str(sync_update_count) + '\n' + \
    #             'sync_count: ' + str(sync_count) + '\n\n' + \
    #             'reg_count_2: ' + str(reg_count_2) + '\n' + \
    #             'sync_update_count_2: ' + str(sync_update_count_2) + '\n' + \
    #             'date_last_sync: ' + str(date_last_sync) + '\n' + \
    #             'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
    #             'Execution time: ' + str(secondsToStr(time() - start)) + '\n'

    def _object_external_sync_2(self, schedule, model_name):

        from time import time
        start = time()

        external_max_task = schedule.external_max_task

        Model = self.env['ir.model']
        ModelFields = self.env['ir.model.fields']

        local_object_model = Model.search([
            ('model', '=', model_name),
        ])

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

            ExternalSync = self.env['clv.external_sync']
            LocalObject = self.env[schedule.model]

            external_object_fields = []
            local_object_fields = []
            for object_field in schedule.object_field_ids:
                external_object_fields.append(object_field.external_object_field)

            external_search_args = []
            if 'active' in external_object_fields:
                external_search_args = [
                    '|',
                    ('active', '=', True),
                    ('active', '=', False),
                ]

            external_object_ids = sock.execute(external_dbname, uid, external_user_pw,
                                               schedule.external_model, 'search', external_search_args)
            _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_object_ids))

            sync_objects = ExternalSync.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('external_id', '!=', False),
                ('external_sync', '!=', 'missing'),
            ])
            _logger.info(u'%s %s', '>>>>>>>>>> (sync_objects):', len(sync_objects))

            missing_count = 0
            for sync_object in sync_objects:
                if sync_object.external_id not in external_object_ids:
                    missing_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>> (missing_object):', missing_count, sync_object.id)
                    sync_object.external_sync = 'missing'

            external_object_fields = sock.execute(external_dbname, uid, external_user_pw,
                                                  schedule.external_model, 'fields_get',
                                                  [], {'attributes': ['string', 'help', 'type']})
            _logger.info(u'%s %s', '>>>>>>>>>> (external_object_fields):', external_object_fields.keys())

            external_args = schedule.external_last_update_args() + external_search_args
            _logger.info(u'%s %s', '>>>>>>>>>> (external_args):', external_args)

            external_object_fields = []
            local_object_fields = []
            for object_field in schedule.object_field_ids:
                if object_field.inclusion is True:
                    external_object_fields.append(object_field.external_object_field)
                    local_object_fields.append(object_field.local_object_field)
            external_object_fields.append('__last_update')
            _logger.info(u'%s %s %s', '>>>>>>>>>> (external_object_fields):',
                         external_object_fields,
                         local_object_fields)
            external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                            schedule.external_model, 'search_read',
                                            external_args,
                                            external_object_fields)

            _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_objects))

            reg_count = 0
            include_count = 0
            update_count = 0
            sync_count = 0
            sync_include_count = 0
            sync_update_count = 0
            task_count = 0
            for external_object in external_objects:

                reg_count += 1

                _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count,
                             external_object['id'],
                             external_object['__last_update'], )

                if task_count >= external_max_task:
                    continue

                if upmost_last_update is False:
                    upmost_last_update = external_object['__last_update']
                else:
                    if external_object['__last_update'] > upmost_last_update:
                        upmost_last_update = external_object['__last_update']

                sync_object = ExternalSync.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('external_id', '=', external_object['id']),
                ])

                if sync_object.id is False:

                    include_count += 1
                    task_count += 1

                    i = 0
                    local_values = {}
                    sync_values = {}
                    for field in local_object_fields:
                        fields = ModelFields.search([
                            ('model_id', '=', local_object_model.id),
                            ('name', '=', local_object_fields[i]),
                        ])

                        if fields[0].ttype in ['char', 'date', 'datetime', 'text', 'integer', 'boolean', 'selection']:
                            local_values[local_object_fields[i]] = external_object[external_object_fields[i]]

                        elif fields[0].ttype == 'many2one':
                            if external_object[external_object_fields[i]] is not False:
                                model_ = fields[0].relation
                                id_ = external_object[external_object_fields[i]][0]
                                # RelationObject = self.env[model_]
                                # relation_object = RelationObject.with_context({'active_test': False}).search([
                                #     ('external_id', '=', int(id_)),
                                # ])
                                relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                    ('model', '=', model_),
                                    ('external_id', '=', int(id_)),
                                ])
                                RelationObject = self.env[model_]
                                relation_object = RelationObject.with_context({'active_test': False}).search([
                                    # ('external_id', '=', int(id_)),
                                    ('id', '=', relation_sync_object.res_id),
                                ])
                                if relation_object.id is not False:
                                    local_values[local_object_fields[i]] = relation_object.id

                        elif fields[0].ttype == 'reference':
                            if external_object[external_object_fields[i]] is not False:
                                model_, id_ = external_object[external_object_fields[i]].split(',')
                                # RefObject = self.env[model_]
                                # ref_object = RefObject.with_context({'active_test': False}).search([
                                #     ('external_id', '=', int(id_)),
                                # ])
                                relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                    ('model', '=', model_),
                                    ('external_id', '=', int(id_)),
                                ])
                                try:
                                    RefObject = self.env[model_]
                                    ref_object = RefObject.with_context({'active_test': False}).search([
                                        # ('external_id', '=', int(id_)),
                                        ('id', '=', relation_sync_object.res_id),
                                    ])
                                    if ref_object.id is not False:
                                        local_values[local_object_fields[i]] = model_ + ',' + str(ref_object.id)
                                except Exception as e:
                                    _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s', e)

                        elif fields[0].ttype == 'many2many':
                            if external_object[external_object_fields[i]] is not False:
                                model_ = fields[0].relation
                                ids_ = external_object[external_object_fields[i]]
                                RelationObject = self.env[model_]

                                m2m_list = []
                                m2m_list.append((5,))
                                for external_id in ids_:
                                    # relation_object = RelationObject.with_context({'active_test': False}).search([
                                    #     ('external_id', '=', external_id),
                                    # ])
                                    relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                        ('model', '=', model_),
                                        ('external_id', '=', int(external_id)),
                                    ])
                                    RelationObject = self.env[model_]
                                    relation_object = RelationObject.with_context({'active_test': False}).search([
                                        # ('external_id', '=', int(id_)),
                                        ('id', '=', relation_sync_object.res_id),
                                    ])
                                    if relation_object.id is not False:
                                        m2m_list.append((4, relation_object.id))

                                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                                local_values[local_object_fields[i]] = m2m_list

                        else:
                            _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)

                        i += 1

                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, local_values)
                    new_local_object = LocalObject.create(local_values)

                    sync_values['model'] = model_name
                    sync_values['res_id'] = new_local_object.id
                    sync_values['external_id'] = external_object['id']
                    sync_values['external_last_update'] = external_object['__last_update']
                    sync_values['external_sync'] = 'included'
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, sync_values)
                    new_sync_object = ExternalSync.create(sync_values)

                    if schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        sync_count += 1
                        sync_include_count += 1
                        task_count += 1

                        new_sync_object._object_synchronize_2(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['id'],
                            schedule, model_name, new_sync_object
                        )

                else:

                    if external_object['__last_update'] > str(sync_object.external_last_update) and \
                       sync_object.external_sync != 'included':

                        update_count += 1
                        task_count += 1

                        sync_object.external_sync = 'updated'

                    if (sync_object.external_sync == 'included' or
                        sync_object.external_sync == 'updated') and \
                       schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        sync_count += 1
                        task_count += 1

                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, sync_object)

                        if sync_object.external_sync == 'included':
                            sync_include_count += 1

                        if sync_object.external_sync == 'updated':
                            sync_update_count += 1

                        sync_object._object_synchronize_2(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['id'],
                            schedule, model_name, sync_object
                        )

            # sync_objects = ExternalSync.with_context({'active_test': False}).search([
            #     ('model', '=', model_name),
            #     ('external_sync', '=', 'updated'),
            # ])
            # _logger.info(u'>>>>>>>>>>>>>>> (sync_objects): %s %s', sync_objects, len(sync_objects))

            # reg_count_2 = 0
            # sync_update_count_2 = 0
            # while len(sync_objects) > 0 and \
            #         sync_count < schedule.external_max_sync:

            #     for external_object in external_objects:

            #         reg_count_2 += 1

            #         _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count_2,
            #                      external_object['id'],
            #                      external_object['__last_update'], )

            #         if upmost_last_update is False:
            #             upmost_last_update = external_object['__last_update']
            #         else:
            #             if external_object['__last_update'] > upmost_last_update:
            #                 upmost_last_update = external_object['__last_update']

            #         sync_object = ExternalSync.with_context({'active_test': False}).search([
            #             ('external_id', '=', external_object['id']),
            #         ])

            #         if sync_object.external_sync == 'updated' and \
            #            schedule.external_exec_sync is True and \
            #            sync_count < schedule.external_max_sync:

            #             sync_count += 1

            #             _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, sync_object)

            #             if sync_object.external_sync == 'updated':
            #                 sync_update_count_2 += 1

            #             sync_object._object_synchronize_2(
            #                 sock, external_dbname, uid, external_user_pw,
            #                 schedule.external_model, external_object['id'],
            #                 schedule, model_name, sync_object
            #             )

            #     sync_objects = ExternalSync.with_context({'active_test': False}).search([
            #         ('model', '=', model_name),
            #         ('external_sync', '=', 'updated'),
            #     ])
            #     _logger.info(u'>>>>>>>>>>>>>>> (sync_objects): %s %s', sync_objects, len(sync_objects))

            _logger.info(u'%s %s', '>>>>>>>>>> external_max_task: ', external_max_task)
            _logger.info(u'%s %s', '>>>>>>>>>> external_exec_sync: ', schedule.external_exec_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> external_max_sync: ', schedule.external_max_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> external_args: ', external_args)
            _logger.info(u'%s %s', '>>>>>>>>>> external_object_ids: ', len(external_object_ids))
            _logger.info(u'%s %s', '>>>>>>>>>> sync_objects: ', len(sync_objects))
            _logger.info(u'%s %s', '>>>>>>>>>> missing_count: ', missing_count)
            _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
            _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_include_count: ', sync_include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count: ', sync_update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_count: ', sync_count)
            # _logger.info(u'%s %s', '>>>>>>>>>> reg_count_2: ', reg_count_2)
            # _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count_2: ', sync_update_count_2)
            _logger.info(u'%s %s', '>>>>>>>>>> task_count: ', task_count)
            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.upmost_last_update = upmost_last_update
            # schedule.external_sync_log +=  \
            #     'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n' + \
            #     'external_max_sync: ' + str(schedule.external_max_sync) + '\n' + \
            #     'external_args: ' + str(external_args) + '\n\n' + \
            #     'external_object_ids: ' + str(len(external_object_ids)) + '\n' + \
            #     'sync_objects: ' + str(len(sync_objects)) + '\n' + \
            #     'missing_count: ' + str(missing_count) + '\n\n' + \
            #     'reg_count: ' + str(reg_count) + '\n' + \
            #     'include_count: ' + str(include_count) + '\n' + \
            #     'update_count: ' + str(update_count) + '\n' + \
            #     'sync_include_count: ' + str(sync_include_count) + '\n' + \
            #     'sync_update_count: ' + str(sync_update_count) + '\n' + \
            #     'sync_count: ' + str(sync_count) + '\n\n' + \
            #     'reg_count_2: ' + str(reg_count_2) + '\n' + \
            #     'sync_update_count_2: ' + str(sync_update_count_2) + '\n' + \
            #     'date_last_sync: ' + str(date_last_sync) + '\n' + \
            #     'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
            #     'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
            schedule.external_sync_log +=  \
                'external_max_task: ' + str(external_max_task) + '\n' + \
                'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n' + \
                'external_max_sync: ' + str(schedule.external_max_sync) + '\n' + \
                'external_args: ' + str(external_args) + '\n\n' + \
                'external_object_ids: ' + str(len(external_object_ids)) + '\n' + \
                'sync_objects: ' + str(len(sync_objects)) + '\n' + \
                'missing_count: ' + str(missing_count) + '\n\n' + \
                'reg_count: ' + str(reg_count) + '\n' + \
                'include_count: ' + str(include_count) + '\n' + \
                'update_count: ' + str(update_count) + '\n' + \
                'sync_include_count: ' + str(sync_include_count) + '\n' + \
                'sync_update_count: ' + str(sync_update_count) + '\n' + \
                'sync_count: ' + str(sync_count) + '\n\n' + \
                'task_count: ' + str(task_count) + '\n\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n'

    def _object_external_recognize(self, schedule, model_name):

        from time import time
        start = time()

        external_max_task = schedule.external_max_task

        Model = self.env['ir.model']
        ModelFields = self.env['ir.model.fields']

        local_object_model = Model.search([
            ('model', '=', model_name),
        ])

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

            ExternalSync = self.env['clv.external_sync']
            LocalObject = self.env[schedule.model]

            external_object_fields = []
            local_object_fields = []
            for object_field in schedule.object_field_ids:
                external_object_fields.append(object_field.external_object_field)

            external_search_args = []
            if 'active' in external_object_fields:
                external_search_args = [
                    '|',
                    ('active', '=', True),
                    ('active', '=', False),
                ]

            external_object_ids = sock.execute(external_dbname, uid, external_user_pw,
                                               schedule.external_model, 'search', external_search_args)
            _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_object_ids))

            sync_objects = ExternalSync.with_context({'active_test': False}).search([
                ('model', '=', model_name),
                ('external_id', '!=', False),
                ('external_sync', '!=', 'missing'),
            ])
            _logger.info(u'%s %s', '>>>>>>>>>> (sync_objects):', len(sync_objects))

            missing_count = 0
            for sync_object in sync_objects:
                if sync_object.external_id not in external_object_ids:
                    missing_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>> (missing_object):', missing_count, sync_object.id)
                    sync_object.external_sync = 'missing'

            external_object_fields = sock.execute(external_dbname, uid, external_user_pw,
                                                  schedule.external_model, 'fields_get',
                                                  [], {'attributes': ['string', 'help', 'type']})
            _logger.info(u'%s %s', '>>>>>>>>>> (external_object_fields):', external_object_fields.keys())

            external_args = schedule.external_last_update_args() + external_search_args
            _logger.info(u'%s %s', '>>>>>>>>>> (external_args):', external_args)

            external_object_fields = []
            local_object_fields = []
            for object_field in schedule.object_field_ids:
                if object_field.inclusion is True:
                    external_object_fields.append(object_field.external_object_field)
                    local_object_fields.append(object_field.local_object_field)
            external_object_fields.append('__last_update')
            _logger.info(u'%s %s %s', '>>>>>>>>>> (external_object_fields):',
                         external_object_fields,
                         local_object_fields)
            external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                            schedule.external_model, 'search_read',
                                            external_args,
                                            external_object_fields)

            _logger.info(u'%s %s', '>>>>>>>>>> (external_objects):', len(external_objects))

            reg_count = 0
            include_count = 0
            update_count = 0
            sync_count = 0
            sync_include_count = 0
            sync_update_count = 0
            task_count = 0
            for external_object in external_objects:

                reg_count += 1

                _logger.info(u'%s %s %s %s', '>>>>>>>>>>', reg_count,
                             external_object['id'],
                             external_object['__last_update'], )

                if task_count >= external_max_task:
                    continue

                if upmost_last_update is False:
                    upmost_last_update = external_object['__last_update']
                else:
                    if external_object['__last_update'] > upmost_last_update:
                        upmost_last_update = external_object['__last_update']

                sync_object = ExternalSync.with_context({'active_test': False}).search([
                    ('model', '=', model_name),
                    ('external_id', '=', external_object['id']),
                ])

                if sync_object.id is False:

                    task_count += 1

                    i = 0
                    local_values = {}
                    sync_values = {}
                    for field in local_object_fields:
                        fields = ModelFields.search([
                            ('model_id', '=', local_object_model.id),
                            ('name', '=', local_object_fields[i]),
                        ])

                        if fields[0].ttype in ['char', 'date', 'datetime', 'text', 'integer', 'boolean', 'selection']:
                            local_values[local_object_fields[i]] = external_object[external_object_fields[i]]

                        elif fields[0].ttype == 'many2one':
                            if external_object[external_object_fields[i]] is not False:
                                model_ = fields[0].relation
                                id_ = external_object[external_object_fields[i]][0]
                                relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                    ('model', '=', model_),
                                    ('external_id', '=', int(id_)),
                                ])
                                RelationObject = self.env[model_]
                                relation_object = RelationObject.with_context({'active_test': False}).search([
                                    ('id', '=', relation_sync_object.res_id),
                                ])
                                if relation_object.id is not False:
                                    local_values[local_object_fields[i]] = relation_object.id

                        elif fields[0].ttype == 'reference':
                            if external_object[external_object_fields[i]] is not False:
                                model_, id_ = external_object[external_object_fields[i]].split(',')
                                relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                    ('model', '=', model_),
                                    ('external_id', '=', int(id_)),
                                ])
                                try:
                                    RefObject = self.env[model_]
                                    ref_object = RefObject.with_context({'active_test': False}).search([
                                        # ('external_id', '=', int(id_)),
                                        ('id', '=', relation_sync_object.res_id),
                                    ])
                                    if ref_object.id is not False:
                                        local_values[local_object_fields[i]] = model_ + ',' + str(ref_object.id)
                                except Exception as e:
                                    _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s', e)

                        elif fields[0].ttype == 'many2many':
                            if external_object[external_object_fields[i]] is not False:
                                model_ = fields[0].relation
                                ids_ = external_object[external_object_fields[i]]
                                RelationObject = self.env[model_]

                                m2m_list = []
                                m2m_list.append((5,))
                                for external_id in ids_:
                                    relation_sync_object = ExternalSync.with_context({'active_test': False}).search([
                                        ('model', '=', model_),
                                        ('external_id', '=', int(external_id)),
                                    ])
                                    RelationObject = self.env[model_]
                                    relation_object = RelationObject.with_context({'active_test': False}).search([
                                        ('id', '=', relation_sync_object.res_id),
                                    ])
                                    if relation_object.id is not False:
                                        m2m_list.append((4, relation_object.id))

                                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                                local_values[local_object_fields[i]] = m2m_list

                        else:
                            _logger.warning(u'>>>>>>>>>>>>>>>>>>>> %s %s', fields[0].name, fields[0].ttype)

                        i += 1

                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, local_values)

                    search_params = []
                    for key in local_values:
                        search_params.append((key, '=', local_values[key]))
                    local_object = LocalObject.with_context({'active_test': False}).search(search_params)

                    if local_object.id is not False:

                        include_count += 1

                        sync_values['model'] = model_name
                        sync_values['res_id'] = local_object.id
                        sync_values['external_id'] = external_object['id']
                        sync_values['external_last_update'] = external_object['__last_update']
                        sync_values['external_sync'] = 'recognized'
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, sync_values)
                        ExternalSync.create(sync_values)

            _logger.info(u'%s %s', '>>>>>>>>>> external_max_task: ', external_max_task)
            _logger.info(u'%s %s', '>>>>>>>>>> external_exec_sync: ', schedule.external_exec_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> external_max_sync: ', schedule.external_max_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> external_args: ', external_args)
            _logger.info(u'%s %s', '>>>>>>>>>> external_object_ids: ', len(external_object_ids))
            _logger.info(u'%s %s', '>>>>>>>>>> sync_objects: ', len(sync_objects))
            _logger.info(u'%s %s', '>>>>>>>>>> missing_count: ', missing_count)
            _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
            _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_include_count: ', sync_include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count: ', sync_update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_count: ', sync_count)
            _logger.info(u'%s %s', '>>>>>>>>>> task_count: ', task_count)
            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.upmost_last_update = upmost_last_update
            schedule.external_sync_log +=  \
                'external_max_task: ' + str(external_max_task) + '\n' + \
                'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n' + \
                'external_max_sync: ' + str(schedule.external_max_sync) + '\n' + \
                'external_args: ' + str(external_args) + '\n\n' + \
                'external_object_ids: ' + str(len(external_object_ids)) + '\n' + \
                'sync_objects: ' + str(len(sync_objects)) + '\n' + \
                'missing_count: ' + str(missing_count) + '\n\n' + \
                'reg_count: ' + str(reg_count) + '\n' + \
                'include_count: ' + str(include_count) + '\n' + \
                'update_count: ' + str(update_count) + '\n' + \
                'sync_include_count: ' + str(sync_include_count) + '\n' + \
                'sync_update_count: ' + str(sync_update_count) + '\n' + \
                'sync_count: ' + str(sync_count) + '\n\n' + \
                'task_count: ' + str(task_count) + '\n\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n'

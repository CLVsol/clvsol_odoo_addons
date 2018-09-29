# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import ssl
import xmlrpc

from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class ExternalSyncModel(models.AbstractModel):
    _name = 'clv.external_sync.model'

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

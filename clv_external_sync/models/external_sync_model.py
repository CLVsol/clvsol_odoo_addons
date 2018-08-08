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
import xmlrpclib

from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class ExternalSyncModel(models.AbstractModel):
    _name = 'clv.external_sync.model'

    external_model = fields.Char(string='External Model')
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

        xmlrpc_sock_common_url = external_host + '/xmlrpc/common'
        xmlrpc_sock_str = external_host + '/xmlrpc/object'

        server_version = False

        login_msg = ''
        user_name = ''
        company_name = ''

        sock_common = xmlrpclib.ServerProxy(xmlrpc_sock_common_url)
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
            sock_common = xmlrpclib.ServerProxy(xmlrpc_sock_common_url)
            uid = sock_common.login(external_dbname, external_user, external_user_pw)
            sock = xmlrpclib.ServerProxy(xmlrpc_sock_str)
        except Exception:
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
            sock_common = xmlrpclib.ServerProxy(xmlrpc_sock_common_url)
            uid = sock_common.login(external_dbname, external_user, external_user_pw)
            sock = xmlrpclib.ServerProxy(xmlrpc_sock_str)
        except Exception:
            pass

        user_fields = ['name', 'parent_id', ]
        user_data = sock.execute(external_dbname, uid, external_user_pw, 'res.users', 'read',
                                 uid, user_fields)
        user_name = user_data['name']
        parent_id = user_data['parent_id']

        if parent_id is not False:
            args = [('id', '=', parent_id[0])]
            company_id = sock.execute(external_dbname, uid, external_user_pw, 'res.company', 'search', args)

            company_fields = ['name', ]
            company_data = sock.execute(external_dbname, uid, external_user_pw, 'res.company', 'read',
                                        company_id[0], company_fields)
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
                                     uid, user_fields)
            user_name = user_data['name']
            parent_id = user_data['parent_id'][0]

            _logger.info(u'%s %s', '>>>>>>>>>>', user_data)

        return uid, sock, login_msg

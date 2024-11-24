# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
# from datetime import datetime
# from functools import reduce
# from ast import literal_eval

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


# def secondsToStr(t):

#     return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSync(models.Model):
    _description = 'External Sync'
    _name = 'clv.external_sync'
    _inherit = 'clv.abstract.external_sync'
    _order = "id desc"

    model = fields.Char(string='Model Name', required=True, index=True)
    res_id = fields.Integer(string='Record ID', help="ID of the target record in the database")
    res_last_update = fields.Datetime(string="Record Last Update")
    reference = fields.Char(string='Reference', compute='_compute_reference', readonly=True, store=True)
    reference_name = fields.Char(string='Reference Name', compute='_compute_reference', readonly=True, store=True)

    @api.depends('model', 'res_id')
    def _compute_reference(self):
        for record in self:
            if record.model is not False and record.res_id > 0:
                record.reference = "%s,%s" % (record.model, record.res_id)
                Model = self.env[record.model]
                rec = Model.search([
                    ('id', '=', record.res_id),
                ])
                try:
                    record.reference_name = rec.name_get()[0][1]
                except IndexError:
                    record.reference_name = str(record.model) + ' ' + str(record.res_id)

    # def _global_settings_sync(self, schedule):

    #     from time import time
    #     start = time()

    #     if schedule.enable_sync:

    #         date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #     method_args = {}
    #     if schedule.method_args is not False:
    #         method_args = literal_eval(schedule.method_args)

    #         remote_object_fields = ['id', 'key', 'value']

    #         AbstractExternalSync = self.env['clv.abstract.external_sync']
    #         IrConfigParameter = self.env['ir.config_parameter']

    #         external_host = schedule.external_host_id.name
    #         external_dbname = schedule.external_host_id.external_dbname
    #         external_user = schedule.external_host_id.external_user
    #         external_user_pw = schedule.external_host_id.external_user_pw

    #         uid, sock, login_msg = AbstractExternalSync.external_sync_host_login(
    #             external_host,
    #             external_dbname,
    #             external_user,
    #             external_user_pw
    #         )
    #         schedule.sync_log += 'login_msg: ' + str(login_msg) + '\n\n'

    #         object_count = 0

    #         if uid is not False:

    #             schedule.sync_log += 'Executing: "' + '_global_settings_sync' + '"...\n\n'

    #             remote_objects = sock.execute(external_dbname, uid, external_user_pw,
    #                                           'ir.config_parameter', 'search_read',
    #                                           [],
    #                                           remote_object_fields)

    #             _logger.info(u'%s %s\n', '--> remote_objects', len(remote_objects))

    #             for remote_object in remote_objects:

    #                 if (remote_object['key'] == method_args['ir.config_parameter.key']):

    #                     object_count += 1

    #                     _logger.info(u'%s %s %s %s', '-->', object_count, remote_object['key'], remote_object['value'])

    #                     local_object = IrConfigParameter.search([('key', '=', remote_object['key'])])

    #                     _logger.info(u'%s %s %s', '---->', local_object['key'], local_object['value'])

    #                     self.env['ir.config_parameter'].set_param(remote_object['key'], remote_object['value'])

    #         _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
    #         _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

    #         schedule.date_last_sync = date_last_sync
    #         schedule.sync_log +=  \
    #             'method_args: ' + str(method_args) + '\n' + \
    #             'object_count: ' + str(object_count) + '\n' + \
    #             'date_last_sync: ' + str(date_last_sync) + '\n' + \
    #             'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

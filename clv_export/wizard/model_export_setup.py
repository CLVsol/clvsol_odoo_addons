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


class ModelExportSetUp(models.TransientModel):
    _name = 'clv.model_export.setup'

    def _default_model_export_ids(self):
        return self._context.get('active_ids')
    model_export_ids = fields.Many2many(
        comodel_name='clv.model_export',
        relation='clv_model_export_setup_rel',
        string='Model Exports',
        default=_default_model_export_ids)

    def _default_dir_path(self):
        ObjectModelExport = self.env['clv.object.model_export']
        return ObjectModelExport.model_export_dir_path('xls')
    dir_path = fields.Char(
        string='Directory Path',
        required=True,
        help="Directory Path",
        default=_default_dir_path
    )

    def _default_file_name(self):
        ObjectModelExport = self.env['clv.object.model_export']
        return ObjectModelExport.model_export_file_name('xls')
    file_name = fields.Char(
        string='File Name',
        required=True,
        help="File Name",
        default=_default_file_name
    )

    def _default_date_format(self):
        ObjectModelExport = self.env['clv.object.model_export']
        return ObjectModelExport.model_export_date_format()
    date_format = fields.Char(
        string='Date Format',
        required=True,
        help="Date Format",
        default=_default_date_format
    )

    def _default_datetime_format(self):
        ObjectModelExport = self.env['clv.object.model_export']
        return ObjectModelExport.model_export_datetime_format()
    datetime_format = fields.Char(
        string='Date Time Format',
        required=True,
        help="Date Time Format",
        default=_default_datetime_format
    )

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
    def do_model_export_setup(self):
        self.ensure_one()

        for model_export in self.model_export_ids:

            _logger.info(u'%s %s', '>>>>>', model_export.name)

            if model_export.export_type == 'xls':
                model_export.do_model_export_execute_xls(self.dir_path, self.file_name)

        return True

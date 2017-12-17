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
# You should have uploadd a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import logging
import base64

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class FileSystemDirectoryFileUpload(models.TransientModel):
    _name = 'clv.file_system.directory.file_upload'

    def _default_file_system_directory_ids(self):
        return self._context.get('active_ids')
    file_system_directory_ids = fields.Many2many(
        comodel_name='clv.file_system.directory',
        relation='clv_file_system_directory_file_upload_rel',
        string='Directories',
        readonly=True,
        default=_default_file_system_directory_ids
    )

    upload_file = fields.Binary(string='Upload File')
    file_name = fields.Char(string='File Name')

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
    def do_file_system_directory_file_upload(self):
        self.ensure_one()

        for file_system_directory in self.file_system_directory_ids:

            _logger.info(u'%s %s', '>>>>>', file_system_directory.name)

            directory = file_system_directory.get_dir() or ''
            full_path = directory + self.file_name

            _logger.info(u'%s %s', '>>>>>>>>>>', full_path)

            f = open(full_path, 'w')
            f.write(base64.decodestring(self.upload_file))
            f.close()

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import os
import base64

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.tools import human_size

_logger = logging.getLogger(__name__)


class LabTestResult(models.Model):
    _inherit = "clv.lab_test.result"

    file_name = fields.Char(string='File Name')
    file_content = fields.Binary(
        string='File Content',
        compute='_compute_file'
    )
    stored_file_name = fields.Char(string='Stored File Name')
    directory_id = fields.Many2one(
        comodel_name='clv.file_system.directory',
        string='Directory'
    )

    def _file_read(self, fname, bin_size=False):

        def file_not_found(fname):
            raise Warning(_(
                '''Error while reading file %s.
                Maybe it was removed or permission is changed.
                Please refresh the list.''' % fname))

        self.ensure_one()
        r = ''
        directory = self.directory_id.get_dir() or ''
        full_path = directory + fname
        if not (directory and os.path.isfile(full_path)):
            # file_not_found(fname)
            return False
        try:
            if bin_size:
                r = human_size(os.path.getsize(full_path))
            else:
                # r = open(full_path, 'rb').read().encode('base64')
                r = base64.b64encode(open(full_path, 'rb').read())
        except (IOError, OSError):
            _logger.info("_read_file reading %s", fname, exc_info=True)
        return r

    @api.depends('stored_file_name')
    def _compute_file(self):
        bin_size = self._context.get('bin_size')
        for file in self:
            file.file_content = False
            if file.stored_file_name:
                content = file._file_read(file.stored_file_name, bin_size)
                file.file_content = content

    file_name_report = fields.Char(string='File Name (Report)')
    file_content_report = fields.Binary(
        string='File Content (Report)',
        compute='_compute_file_report'
    )
    stored_file_name_report = fields.Char(string='Stored File Name (Report)')
    directory_id_report = fields.Many2one(
        comodel_name='clv.file_system.directory',
        string='Directory (Report)'
    )

    def _file_read_report(self, fname, bin_size=False):

        def file_not_found(fname):
            raise Warning(_(
                '''Error while reading file %s.
                Maybe it was removed or permission is changed.
                Please refresh the list.''' % fname))

        self.ensure_one()
        r = ''
        directory = self.directory_id_report.get_dir() or ''
        full_path = directory + fname
        if not (directory and os.path.isfile(full_path)):
            # file_not_found(fname)
            return False
        try:
            if bin_size:
                r = human_size(os.path.getsize(full_path))
            else:
                # r = open(full_path, 'rb').read().encode('base64')
                r = base64.b64encode(open(full_path, 'rb').read())
        except (IOError, OSError):
            _logger.info("_read_file reading %s", fname, exc_info=True)
        return r

    @api.depends('stored_file_name_report')
    def _compute_file_report(self):
        bin_size = self._context.get('bin_size')
        for file in self:
            file.file_content_report = False
            if file.stored_file_name_report:
                content = file._file_read_report(file.stored_file_name_report, bin_size)
                file.file_content_report = content

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultExportXLS(models.TransientModel):
    _description = 'Lab Test Result Export XLS'
    _name = 'clv.lab_test.result.export_xls'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_export_xls_rel',
        string='Lab Test Results',
        default=_default_lab_test_result_ids
    )

    def _default_dir_path_result(self):
        file_store_path = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_filestore_path', '').strip()
        lab_test_result_files_directory_xls = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_lab_test_result_files_directory_xls', '').strip()
        return file_store_path + '/' + lab_test_result_files_directory_xls
    dir_path_result = fields.Char(
        string='Directory Path (Result)',
        required=True,
        help="Directory Path (Result)",
        default=_default_dir_path_result
    )

    def _default_file_name_result(self):
        lab_test_result_file_name_xls = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_lab_test_result_file_name_xls', '').strip()
        return lab_test_result_file_name_xls
    file_name_result = fields.Char(
        string='File Name (Result)',
        required=True,
        help="File Name (Result)",
        default=_default_file_name_result
    )

    use_template_result = fields.Boolean(string='Use Template (Result)', default=True)

    def _default_templates_dir_path_result(self):
        file_store_path = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_filestore_path', '').strip()
        lab_test_result_files_directory_templates = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_lab_test_result_files_directory_templates', '').strip()
        return file_store_path + '/' + lab_test_result_files_directory_templates
    templates_dir_path_result = fields.Char(
        string='Template Directory Path (Result)',
        required=True,
        help="Template Directory Path (Result)",
        default=_default_templates_dir_path_result
    )

    def do_lab_test_result_export_xls(self):
        self.ensure_one()

        for lab_test_result_reg in self.lab_test_result_ids:

            _logger.info(u'%s %s', '>>>>>', lab_test_result_reg.code)

            lab_test_result_reg.lab_test_result_export_xls(self.dir_path_result, self.file_name_result,
                                                           self.use_template_result, self.templates_dir_path_result)

        return True

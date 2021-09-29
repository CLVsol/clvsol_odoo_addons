# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyExport(models.TransientModel):
    _description = 'Survey Export'
    _name = 'clv.survey.export'

    def _default_survey_ids(self):
        return self._context.get('active_ids')
    survey_ids = fields.Many2many(
        comodel_name='survey.survey',
        relation='clv_survey_export_rel',
        string='Surveys',
        default=_default_survey_ids
    )

    def _default_dir_path(self):
        dir_path = \
            self.env['ir.config_parameter'].sudo().get_param(
                'clv.global_settings.current_filestore_path', '').strip() + \
            '/' + \
            self.env['ir.config_parameter'].sudo().get_param(
                'clv.global_settings.current_survey_files_directory_templates', '').strip()

        return dir_path
    dir_path = fields.Char(
        'Directory Path',
        required=True,
        help="Directory Path",
        default=_default_dir_path
    )

    file_name = fields.Char(
        'File Name',
        required=True,
        help="File Name",
        default='survey_jcafb_<code>.xml'
    )

    export_xml = fields.Boolean(
        string='XML File Export',
        default=False,
        readonly=False
    )

    export_yaml = fields.Boolean(
        string='YAML File Export',
        default=False,
        readonly=False
    )

    export_txt = fields.Boolean(
        string='TXT File Export',
        default=False,
        readonly=False
    )

    def do_survey_export(self):
        self.ensure_one()

        for survey_reg in self.survey_ids:

            xml_file_path = False
            yaml_file_path = False
            txt_file_path = False
            xls_file_path = False

            if self.export_xml is True:

                xml_file_path = self.dir_path + '/' + \
                    self.file_name.replace('<code>', survey_reg.code)
                # _logger.info(u'%s %s', '>>>>>', xml_file_path)

            if self.export_yaml is True:

                yaml_file_path = self.dir_path + '/' + \
                    self.file_name.replace('<code>', survey_reg.code).replace('.xml', '.yaml')
                # _logger.info(u'%s %s', '>>>>>', yaml_file_path)

            if self.export_txt is True:

                txt_file_path = self.dir_path + '/' + \
                    self.file_name.replace('<code>', survey_reg.code).replace('.xml', '.txt')
                # _logger.info(u'%s %s', '>>>>>', txt_file_path)

            survey_reg.survey_survey_export(
                yaml_filepath=yaml_file_path,
                xml_filepath=xml_file_path,
                txt_filepath=txt_file_path,
                xls_filepath=xls_file_path
            )

        return True

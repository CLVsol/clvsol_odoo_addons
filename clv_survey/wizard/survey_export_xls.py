# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import xlwt

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyExportXLS(models.TransientModel):
    _description = 'Survey Export XLS'
    _name = 'clv.survey.export_xls'

    def _default_survey_ids(self):
        return self._context.get('active_ids')
    survey_ids = fields.Many2many(
        comodel_name='survey.survey',
        relation='clv_survey_export_xls_rel',
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
        string='Directory Path',
        required=True,
        help="Directory Path",
        default=_default_dir_path
    )

    file_name = fields.Char(
        string='File Name',
        required=True,
        help="File Name",
        default='<code>_nnn.nnn-dd_<file_format>.xls'
    )

    password = fields.Char(
        string='Password',
        required=True,
        help="Password to protec the sheet",
        default='OpenSesame'
    )

    file_format = fields.Selection(
        [('draft', 'Draft'),
         ('preformatted', 'Preformatted'),
         ], string='File Format', default='draft'
    )

    def do_survey_export_xls(self):
        self.ensure_one()

        style_text_locked = xlwt.easyxf('''
            border: bottom THIN;
        ''')

        style_text_unlocked = xlwt.easyxf('''
            border: bottom THIN;
            protection: cell_locked false;
            font: bold on;
        ''')

        style_choice_thin = xlwt.easyxf('''
            font: bold on;
            borders: left THIN, right THIN, top THIN, bottom THIN;
            align: vertical center, horizontal center;
            protection: cell_locked false;
        ''')

        style_choice_dotted = xlwt.easyxf('''
            font: bold on;
            borders: left DOTTED, right DOTTED, top DOTTED, bottom DOTTED;
            align: vertical center, horizontal center;
            protection: cell_locked false;
        ''')

        style_dot = xlwt.easyxf('''
            align: vertical center, horizontal right;
        ''')

        isHidden = False
        if self.file_format == 'preformatted':
            isHidden = True

        SurveyQuestion = self.env['survey.question']

        for survey_reg in self.survey_ids:

            file_path = self.dir_path + '/' + \
                self.file_name.replace('<code>', survey_reg.code).replace('<file_format>', self.file_format)

            _logger.info(u'%s %s', '>>>>>', file_path)

            book = xlwt.Workbook()

            _title_ = survey_reg.title
            _description_ = survey_reg.description.replace('<p>', '').replace('</p>', '')

            row_nr = 0
            sheet = book.add_sheet(survey_reg.code)
            row = sheet.row(row_nr)
            row.write(0, '[' + survey_reg.code + ']')
            row_nr += 1

            row = sheet.row(row_nr)
            row.write(0, '[' + survey_reg.code + ']')
            row.write(2, _title_)
            row_nr += 1
            row = sheet.row(row_nr)
            row.write(0, '[' + survey_reg.code + ']')
            row.write(2, _description_)
            row_nr += 2

            pages = SurveyQuestion.search([
                ('survey_id', '=', survey_reg.id),
                ('is_page', '=', True),
            ])

            # for page in survey_reg.page_ids:
            for page in pages:

                _title_ = page.title
                _description_ = False
                if page.description is not False:
                    _description_ = page.description.replace('<p>', '').replace('</p>', '')

                row = sheet.row(row_nr)
                row.write(0, '[' + page.code + ']')
                row.write(3, _title_)
                row_nr += 1
                row = sheet.row(row_nr)
                row.write(0, '[' + page.code + ']')
                row.write(3, _description_)
                row_nr += 2

                for question in page.question_ids:

                    question_type = question.question_type
                    _title_ = question.title
                    if question.comments_message is not False:
                        _comments_message_ = question.comments_message
                    if question.comments_allowed is False:
                        _comments_message_ = ''

                    if question_type == 'char_box' or question_type == 'text_box' or question_type == 'datetime':

                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, _title_)
                        row_nr += 1
                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, question_type)
                        row.hidden = isHidden
                        row_nr += 2
                        if question_type == 'free_text':
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(4, '.', style=style_dot)
                            row.write(5, None, style=style_text_unlocked)
                            for i in range(6, 15):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(4, '.', style=style_dot)
                            row.write(5, None, style=style_text_unlocked)
                            for i in range(6, 15):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(4, '.', style=style_dot)
                            row.write(5, None, style=style_text_unlocked)
                            for i in range(6, 15):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(4, '.', style=style_dot)
                            row.write(5, None, style=style_text_unlocked)
                            for i in range(6, 15):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 1
                        else:
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(4, '.', style=style_dot)

                            row.write(5, None, style=style_text_unlocked)
                            for i in range(6, 15):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 1
                        row_nr += 1

                    if question_type == 'simple_choice':

                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, _title_)
                        row_nr += 1
                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, question_type)
                        row.hidden = isHidden
                        row_nr += 2

                        for question_answer in question.suggested_answer_ids:

                            _value_ = question_answer.value

                            row = sheet.row(row_nr)
                            row.write(0, '[' + question_answer.code + ']')
                            row.write(4, '.', style=style_dot)
                            row.write(5, None, style=style_choice_thin)
                            row.write(6, _value_)
                            row_nr += 1

                        if question.comments_allowed is True:
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(6, _comments_message_)
                            row_nr += 2
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(6, '.', style=style_dot)
                            row.write(7, None, style=style_text_unlocked)
                            for i in range(8, 17):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 2
                        else:
                            row_nr += 1

                    if question_type == 'multiple_choice':

                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, _title_)
                        row_nr += 1
                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, question_type)
                        row.hidden = isHidden
                        row_nr += 2

                        for question_answer in question.suggested_answer_ids:

                            _value_ = question_answer.value

                            row = sheet.row(row_nr)
                            row.write(0, '[' + question_answer.code + ']')
                            row.write(4, '.', style=style_dot)
                            row.write(5, None, style=style_choice_dotted)
                            row.write(6, _value_)
                            row_nr += 1

                        if question.comments_allowed is True:
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(6, _comments_message_)
                            row_nr += 2
                            row = sheet.row(row_nr)
                            row.write(0, '[' + question.code + ']')
                            row.write(6, '.', style=style_dot)
                            row.write(7, None, style=style_text_unlocked)
                            for i in range(8, 17):
                                row.write(i, None, style=style_text_locked)
                            row_nr += 2
                        else:
                            row_nr += 1

                    if question_type == 'matrix':

                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, _title_)
                        row_nr += 1
                        row = sheet.row(row_nr)
                        row.write(0, '[' + question.code + ']')
                        row.write(4, question_type + '_' + question.matrix_subtype)
                        row.hidden = isHidden
                        row_nr += 1

                        row_nr += 1
                        matrix_col_row_nr = row_nr
                        matrix_col_nr = 8
                        matrix_row_nrs = []
                        row_nr += 3

                        row_matrix_col = sheet.row(matrix_col_row_nr)
                        row_matrix_col.write(0, '[]')
                        sheet.row(matrix_col_row_nr).hidden = isHidden

                        for matrix_row in question.matrix_row_ids:

                            _value_ = matrix_row.value

                            row = sheet.row(row_nr)
                            row.write(0, '[' + matrix_row.code + ']')
                            row.write(5, _value_)
                            matrix_row_nrs = matrix_row_nrs + [row_nr]
                            row_nr += 2

                        for question_answer in question.suggested_answer_ids:

                            _value_ = question_answer.value

                            row = sheet.row(matrix_col_row_nr)
                            row.write(matrix_col_nr, '[' + question_answer.code + ']')
                            row = sheet.row(matrix_col_row_nr + 1)
                            row.write(matrix_col_nr + 1, _value_)
                            for matrix_row_nr in matrix_row_nrs:
                                row = sheet.row(matrix_row_nr)
                                row.write(matrix_col_nr, '.', style=style_dot)
                                row.write(matrix_col_nr + 1, None, style=style_choice_thin)
                            matrix_col_nr += 3

                        row_nr += 1

            sheet.col(0).hidden = isHidden

            if self.file_format == 'preformatted':

                for i in range(100):
                    sheet.col(i).width = 256 * 2

                sheet.protect = True
                sheet.password = self.password

            book.save(file_path)

        return True

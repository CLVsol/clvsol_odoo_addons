# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import xlwt

from odoo import models

_logger = logging.getLogger(__name__)


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    def survey_survey_export(
        self, yaml_filepath=False, xml_filepath=False, txt_filepath=False,
        xls_filepath=False, file_format=False, password=False
    ):
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
        if file_format == 'preformatted':
            isHidden = True

        export_yaml = False
        export_txt = False
        export_xml = False
        export_xls = False

        yaml_file = False
        txt_file = False
        xml_file = False
        # xls_file = False
        book = False
        row_nr = 0

        if yaml_filepath:
            export_yaml = True
            _logger.info(u'%s %s', '>>>>>', yaml_filepath)
            yaml_file = open(yaml_filepath, "w")

        if txt_filepath:
            export_txt = True
            _logger.info(u'%s %s', '>>>>>', txt_filepath)
            txt_file = open(txt_filepath, "w")

        if xml_filepath:
            export_xml = True
            _logger.info(u'%s %s', '>>>>>', xml_filepath)
            xml_file = open(xml_filepath, "w")

        if xls_filepath:
            _logger.info(u'%s %s', '>>>>>', xls_filepath)
            export_xls = True
            book = xlwt.Workbook()

        def survey():

            SurveyQuestion = self.env['survey.question']

            _survey_title_ = self.title
            _survey_model_ = 'survey.survey'
            _survey_state_ = self.state
            _survey_code_ = self.code
            _survey_users_login_required_ = self.users_login_required
            _survey_attempts_limit_ = self.attempts_limit
            _survey_users_can_go_back_ = self.users_can_go_back
            _survey_description_ = False
            if self.description is not False and self.description != '<p><br></p>' and self.description != '<br>':
                _survey_description_ = self.description.replace('<p>', '').replace('</p>', '')
            _survey_questions_layout_ = self.questions_layout
            _survey_progression_mode_ = self.progression_mode
            _survey_is_time_limited_ = self.is_time_limited
            _survey_questions_selection_ = self.questions_selection

            def survey_page(page):

                _page_title_ = page.title
                _page_model_ = 'survey.question'
                _page_code_ = page.code
                _is_page_ = page.is_page
                _page_parameter_ = page.parameter
                _page_sequence_ = page.sequence
                _page_description_ = False
                if page.description is not False and page.description != '<p><br></p>' and self.description != '<br>':
                    _page_description_ = page.description.replace('<p>', '').replace('</p>', '')

                def survey_question(question):

                    _question_type_ = question.question_type
                    _question_title_ = question.title
                    _question_model_ = 'survey.question'
                    if question.comments_message is not False:
                        _question_comments_message_ = question.comments_message
                    if question.comments_allowed is False:
                        _question_comments_message_ = ''

                    _is_page_ = question.is_page
                    _question_code_ = question.code
                    _question_parameter_ = question.parameter
                    _question_sequence_ = question.sequence
                    _question_description_ = False
                    if question.description is not False and question.description != '<p><br></p>' \
                       and question.description != '<br>':
                        _question_description_ = question.description.replace('<p>', '').replace('</p>', '')
                    _question_constr_mandatory_ = question.constr_mandatory
                    _question_constr_error_msg_ = question.constr_error_msg
                    _question_comment_count_as_answer_ = question.comment_count_as_answer
                    _question_column_nb_ = question.column_nb
                    _question_comments_allowed_ = question.comments_allowed
                    _question_matrix_subtype_ = question.matrix_subtype

                    def survey_question_answer(question_answer):

                        _question_answer_model_ = 'survey.question.answer'
                        _question_answer_code_ = question_answer.code
                        _question_answer_value_ = question_answer.value
                        _question_answer_sequence_ = question_answer.sequence

                        if export_xml:

                            xml_file.write('                    <record model="%s" id="%s">\n' %
                                           (_question_answer_model_, _question_answer_code_))
                            xml_file.write('                        <field name="value">%s</field>\n' %
                                           (_question_answer_value_))
                            xml_file.write('                        <field name="code">%s</field>\n' %
                                           (_question_answer_code_))
                            xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                           (_question_code_))
                            xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                           (_question_answer_sequence_))
                            xml_file.write('                    </record>\n')
                            xml_file.write('\n')

                        if export_yaml:

                            if _question_type_ != 'matrix':

                                yaml_file.write('            %s:\n' % (_question_answer_code_))
                                yaml_file.write('                model: %s\n' % (_question_answer_model_))
                                yaml_file.write('                value: \'%s\'\n' % (_question_answer_value_))
                                yaml_file.write('                code: \'%s\'\n' % (_question_answer_code_))
                                yaml_file.write('                question_id: %s\n' % (_question_code_))
                                yaml_file.write('                sequence: %s\n' % (_question_answer_sequence_))

                        if export_txt:

                            txt_file.write('            %s\n' % (_question_answer_value_))

                    def survey_question_matrix_row(question_matrix_row):

                        _question_answer_model_ = 'survey.question.answer'
                        _matrix_row_code_ = matrix_row.code
                        _matrix_row_value_ = matrix_row.value
                        _matrix_row_sequence_ = matrix_row.sequence

                        if export_xml:

                            xml_file.write('                    <record model="%s" id="%s">\n' %
                                           (_question_answer_model_, _matrix_row_code_))
                            xml_file.write('                        <field name="value">%s</field>\n' %
                                           (_matrix_row_value_))
                            xml_file.write('                        <field name="code">%s</field>\n' % (_matrix_row_code_))
                            xml_file.write('                        <field name="matrix_question_id" ref="%s"/>\n' %
                                           (_question_code_))
                            xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                           (_matrix_row_sequence_))
                            xml_file.write('                    </record>\n')
                            xml_file.write('\n')

                        if export_txt:

                            txt_file.write('            %s\n' % (_matrix_row_value_))

                    nonlocal row_nr

                    if _question_type_ == 'char_box' or _question_type_ == 'text_box' or _question_type_ == 'datetime':

                        if export_xml:

                            xml_file.write('                <!-- %s -->\n' % (_question_title_))
                            xml_file.write('                <record model="%s" id="%s">\n' % (_question_model_, _question_code_))
                            xml_file.write('                    <field name="title">%s</field>\n' % (_question_title_))
                            xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (_is_page_))
                            xml_file.write('                    <field name="code">%s</field>\n' % (_question_code_))
                            if question.parameter:
                                xml_file.write('                    <field name="parameter">%s</field>\n' %
                                               (_question_parameter_))
                            xml_file.write('                    <field name="question_type">%s</field>\n' % (_question_type_))
                            xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (_survey_code_))
                            xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                               (_question_description_))
                            xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                           (_question_constr_mandatory_))
                            xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                           (_question_constr_error_msg_))
                            xml_file.write('                </record>\n')
                            xml_file.write('\n')

                        if export_yaml:

                            yaml_file.write('        %s:\n' % (_question_code_))
                            yaml_file.write('            model: %s\n' % (_question_model_))
                            yaml_file.write('            title: \'%s\'\n' % (_question_title_))
                            yaml_file.write('            is_page: %s\n' % (_is_page_))
                            yaml_file.write('            code: \'%s\'\n' % (_question_code_))
                            if question.parameter:
                                yaml_file.write('            parameter: \'%s\'\n' % (_question_parameter_))
                            yaml_file.write('            question_type: \'%s\'\n' % (_question_type_))
                            yaml_file.write('            survey_id: %s\n' % (_survey_code_))
                            yaml_file.write('            sequence: %s\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                yaml_file.write('            description: \'%s\'\n' % (_question_description_))
                            yaml_file.write('            constr_mandatory: %s\n' % (_question_constr_mandatory_))
                            yaml_file.write('            constr_error_msg: \'%s\'\n' % (_question_constr_error_msg_))
                            yaml_file.write('\n')

                        if export_txt:

                            txt_file.write('        %s\n' % (_question_title_))
                            if _question_description_ is not False:
                                txt_file.write('        %s\n\n' % (_question_description_))
                            else:
                                txt_file.write('\n')
                            txt_file.write('            (%s)\n' % (_question_type_))
                            if _question_type_ == 'text_box':
                                txt_file.write('            ' + '____________________________________\n' +
                                               '            ' + '____________________________________\n' +
                                               '            ' + '____________________________________\n' +
                                               '            ' + '____________________________________\n')
                            else:
                                txt_file.write('            ' + '____________________________________\n')
                            txt_file.write('\n')

                        if export_xls:

                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_title_)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_type_)
                            row.hidden = isHidden
                            row_nr += 2
                            if _question_type_ == 'text_box':
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(4, '.', style=style_dot)
                                row.write(5, None, style=style_text_unlocked)
                                for i in range(6, 15):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 1
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(4, '.', style=style_dot)
                                row.write(5, None, style=style_text_unlocked)
                                for i in range(6, 15):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 1
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(4, '.', style=style_dot)
                                row.write(5, None, style=style_text_unlocked)
                                for i in range(6, 15):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 1
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(4, '.', style=style_dot)
                                row.write(5, None, style=style_text_unlocked)
                                for i in range(6, 15):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 1
                            else:
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(4, '.', style=style_dot)

                                row.write(5, None, style=style_text_unlocked)
                                for i in range(6, 15):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 1
                            row_nr += 1

                    if _question_type_ == 'simple_choice':

                        if export_xml:

                            xml_file.write('                <!-- %s -->\n' % (_question_title_))
                            xml_file.write('                <record model="%s" id="%s">\n' % (_question_model_, _question_code_))
                            xml_file.write('                    <field name="title">%s</field>\n' % (_question_title_))
                            xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (_is_page_))
                            xml_file.write('                    <field name="code">%s</field>\n' % (_question_code_))
                            if question.parameter:
                                xml_file.write('                    <field name="parameter">%s</field>\n' %
                                               (_question_parameter_))
                            xml_file.write('                    <field name="question_type">%s</field>\n' % (_question_type_))
                            xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (_survey_code_))
                            xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                               (_question_description_))
                            xml_file.write('                    <field name="column_nb">%s</field>\n' %
                                           (_question_column_nb_))
                            xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                           (_question_constr_mandatory_))
                            xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                           (_question_constr_error_msg_))
                            xml_file.write('                    <field name="comments_allowed">%s</field>\n' %
                                           (_question_comments_allowed_))
                            xml_file.write('                    <field name="comments_message">%s</field>\n' %
                                           (_question_comments_message_))
                            xml_file.write('                    <field name="comment_count_as_answer">%s</field>\n' %
                                           (_question_comment_count_as_answer_))
                            xml_file.write('                </record>\n')
                            xml_file.write('\n')

                        if export_yaml:

                            yaml_file.write('        %s:\n' % (_question_code_))
                            yaml_file.write('            model: %s\n' % (_question_model_))
                            yaml_file.write('            title: \'%s\'\n' % (_question_title_))
                            yaml_file.write('            is_page: %s\n' % (_is_page_))
                            yaml_file.write('            code: \'%s\'\n' % (_question_code_))
                            if question.parameter:
                                yaml_file.write('            parameter: \'%s\'\n' % (_question_parameter_))
                            yaml_file.write('            question_type: \'%s\'\n' % (_question_type_))
                            yaml_file.write('            survey_id: %s\n' % (_survey_code_))
                            yaml_file.write('            sequence: %s\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                yaml_file.write('            description: \'%s\'\n' % (_question_description_))
                            yaml_file.write('            column_nb: %s\n' % (_question_column_nb_))
                            yaml_file.write('            constr_mandatory: %s\n' % (_question_constr_mandatory_))
                            yaml_file.write('            constr_error_msg: \'%s\'\n' % (_question_constr_error_msg_))
                            yaml_file.write('            comments_allowed: %s\n' % (_question_comments_allowed_))
                            yaml_file.write('            comments_message: \'%s\'\n' % (_question_comments_message_))
                            yaml_file.write('            comment_count_as_answer: %s\n' % (_question_comment_count_as_answer_))
                            yaml_file.write('\n')

                        if export_txt:

                            txt_file.write('        %s\n' % (_question_title_))
                            if _question_description_ is not False:
                                txt_file.write('        %s\n\n' % (_question_description_))
                            else:
                                txt_file.write('\n')
                            txt_file.write('            (%s)\n' % (_question_type_))

                        for question_answer in question.suggested_answer_ids:

                            survey_question_answer(question_answer)

                        if export_yaml:

                            yaml_file.write('\n')

                        if export_txt:

                            if _question_comments_allowed_ == 'True':
                                txt_file.write('            %s____________________________________\n\n' %
                                               (_question_comments_message_))
                            else:
                                txt_file.write('\n')

                        if export_xls:

                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_title_)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_type_)
                            row.hidden = isHidden
                            row_nr += 2

                            for question_answer in question.suggested_answer_ids:

                                _question_answer_code_ = question_answer.code
                                _question_answer_value_ = question_answer.value

                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_answer_code_ + ']')
                                row.write(4, '.', style=style_dot)
                                row.write(5, None, style=style_choice_thin)
                                row.write(6, _question_answer_value_)
                                row_nr += 1

                            if question.comments_allowed is True:
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(6, _question_comments_message_)
                                row_nr += 2
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(6, '.', style=style_dot)
                                row.write(7, None, style=style_text_unlocked)
                                for i in range(8, 17):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 2
                            else:
                                row_nr += 1

                    if _question_type_ == 'multiple_choice':

                        if export_xml:

                            xml_file.write('                <!-- %s -->\n' % (_question_title_))
                            xml_file.write('                <record model="%s" id="%s">\n' % (_question_model_, _question_code_))
                            xml_file.write('                    <field name="title">%s</field>\n' % (_question_title_))
                            xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (_is_page_))
                            xml_file.write('                    <field name="code">%s</field>\n' % (_question_code_))
                            if question.parameter:
                                xml_file.write('                    <field name="parameter">%s</field>\n' %
                                               (_question_parameter_))
                            xml_file.write('                    <field name="question_type">%s</field>\n' % (_question_type_))
                            xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (_survey_code_))
                            xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                               (_question_description_))
                            xml_file.write('                    <field name="column_nb">%s</field>\n' %
                                           (_question_column_nb_))
                            xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                           (_question_constr_mandatory_))
                            xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                           (_question_constr_error_msg_))
                            xml_file.write('                    <field name="comments_allowed">%s</field>\n' %
                                           (question.comments_allowed))
                            xml_file.write('                    <field name="comments_message">%s</field>\n' %
                                           (_question_comments_message_))
                            xml_file.write('                    <field name="comment_count_as_answer">%s</field>\n' %
                                           (_question_comment_count_as_answer_))
                            xml_file.write('                </record>\n')
                            xml_file.write('\n')

                        if export_yaml:

                            yaml_file.write('        %s:\n' % (_question_code_))
                            yaml_file.write('            model: %s\n' % (_question_model_))
                            yaml_file.write('            title: \'%s\'\n' % (_question_title_))
                            yaml_file.write('            is_page: %s\n' % (_is_page_))
                            yaml_file.write('            code: \'%s\'\n' % (_question_code_))
                            if question.parameter:
                                yaml_file.write('            parameter: \'%s\'\n' % (_question_parameter_))
                            yaml_file.write('            question_type: \'%s\'\n' % (_question_type_))
                            yaml_file.write('            survey_id: %s\n' % (_survey_code_))
                            yaml_file.write('            sequence: %s\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                yaml_file.write('            description: \'%s\'\n' % (_question_description_))
                            yaml_file.write('            column_nb: %s\n' % (_question_column_nb_))
                            yaml_file.write('            constr_mandatory: %s\n' % (_question_constr_mandatory_))
                            yaml_file.write('            constr_error_msg: \'%s\'\n' % (_question_constr_error_msg_))
                            yaml_file.write('            comments_allowed: %s\n' % (_question_comments_allowed_))
                            yaml_file.write('            comments_message: \'%s\'\n' % (_question_comments_message_))
                            yaml_file.write('            comment_count_as_answer: %s\n' % (_question_comment_count_as_answer_))
                            yaml_file.write('\n')

                        if export_txt:

                            txt_file.write('        %s\n' % (_question_title_))
                            if _question_description_ is not False:
                                txt_file.write('        %s\n\n' % (_question_description_))
                            else:
                                txt_file.write('\n')
                            txt_file.write('            (%s)\n' % (_question_type_))

                        for question_answer in question.suggested_answer_ids:

                            survey_question_answer(question_answer)

                        if export_yaml:

                            yaml_file.write('\n')

                        if export_txt:

                            if _question_comments_allowed_ == 'True':
                                txt_file.write('            %s____________________________________\n\n' %
                                               (_question_comments_message_))
                            else:
                                txt_file.write('\n')

                        if export_xls:

                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_title_)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_type_)
                            row.hidden = isHidden
                            row_nr += 2

                            for question_answer in question.suggested_answer_ids:

                                _question_answer_code_ = question_answer.code
                                _question_answer_value_ = question_answer.value

                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_answer_code_ + ']')
                                row.write(4, '.', style=style_dot)
                                row.write(5, None, style=style_choice_dotted)
                                row.write(6, _question_answer_value_)
                                row_nr += 1

                            if question.comments_allowed is True:
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(6, _question_comments_message_)
                                row_nr += 2
                                row = sheet.row(row_nr)
                                row.write(0, '[' + _question_code_ + ']')
                                row.write(6, '.', style=style_dot)
                                row.write(7, None, style=style_text_unlocked)
                                for i in range(8, 17):
                                    row.write(i, None, style=style_text_locked)
                                row_nr += 2
                            else:
                                row_nr += 1

                    if _question_type_ == 'matrix':

                        if export_xml:

                            xml_file.write('                <!-- %s -->\n' % (_question_title_))
                            xml_file.write('                <record model="%s" id="%s">\n' % (_question_model_, _question_code_))
                            xml_file.write('                    <field name="title">%s</field>\n' % (_question_title_))
                            xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (_is_page_))
                            xml_file.write('                    <field name="code">%s</field>\n' % (_question_code_))
                            if question.parameter:
                                xml_file.write('                    <field name="parameter">%s</field>\n' %
                                               (_question_parameter_))
                            xml_file.write('                    <field name="question_type">%s</field>\n' % (_question_type_))
                            xml_file.write('                    <field name="matrix_subtype">%s</field>\n' %
                                           (_question_matrix_subtype_))
                            xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (_survey_code_))
                            xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                               (_question_description_))
                            xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                           (_question_constr_mandatory_))
                            xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                           (_question_constr_error_msg_))
                            xml_file.write('                </record>\n')
                            xml_file.write('\n')

                            for question_answer in question.suggested_answer_ids:

                                survey_question_answer(question_answer)

                            for matrix_row in question.matrix_row_ids:

                                survey_question_matrix_row(matrix_row)

                        if export_txt:

                            txt_file.write('        %s\n' % (_question_title_))
                            if _question_description_ is not False:
                                txt_file.write('        %s\n\n' % (_question_description_))
                            else:
                                txt_file.write('\n')
                            txt_file.write('            (%s -  %s)\n\n' % (_question_type_, _question_matrix_subtype_))

                            for question_answer in question.suggested_answer_ids:

                                survey_question_answer(question_answer)

                            txt_file.write('\n')

                            for matrix_row in question.matrix_row_ids:

                                survey_question_matrix_row(matrix_row)

                            txt_file.write('\n')

                        if export_yaml:

                            yaml_file.write('        %s:\n' % (_question_code_))
                            yaml_file.write('            model: %s\n' % (_question_model_))
                            yaml_file.write('            title: \'%s\'\n' % (_question_title_))
                            yaml_file.write('            is_page: %s\n' % (_is_page_))
                            yaml_file.write('            code: \'%s\'\n' % (_question_code_))
                            if question.parameter:
                                yaml_file.write('            parameter: \'%s\'\n' % (_question_parameter_))
                            yaml_file.write('            question_type: \'%s\'\n' % (_question_type_))
                            yaml_file.write('            matrix_subtype: \'%s\'\n' % (_question_matrix_subtype_))
                            yaml_file.write('            survey_id: %s\n' % (_survey_code_))
                            yaml_file.write('            sequence: %s\n' % (_question_sequence_))
                            if _question_description_ is not False:
                                yaml_file.write('            description: \'%s\'\n' % (_question_description_))
                            yaml_file.write('            column_nb: %s\n' % (_question_column_nb_))
                            yaml_file.write('            constr_mandatory: %s\n' % (_question_constr_mandatory_))
                            yaml_file.write('            constr_error_msg: \'%s\'\n' % (_question_constr_error_msg_))
                            yaml_file.write('\n')

                            for matrix_row in question.matrix_row_ids:

                                _question_answer_model_ = 'survey.question.answer'
                                _matrix_row_code_ = matrix_row.code
                                _matrix_row_value_ = matrix_row.value
                                _matrix_row_sequence_ = matrix_row.sequence

                                yaml_file.write('            %s:\n' % (_matrix_row_code_))
                                yaml_file.write('                model: %s\n' % (_question_answer_model_))
                                yaml_file.write('                value: \'%s\'\n' % (_matrix_row_value_))
                                yaml_file.write('                code: \'%s\'\n' % (_matrix_row_code_))
                                yaml_file.write('                matrix_question_id: %s\n' % (_question_code_))
                                yaml_file.write('                sequence: %s\n' % (_matrix_row_sequence_))

                            yaml_file.write('\n')

                            for question_answer in question.suggested_answer_ids:

                                _question_answer_model_ = 'survey.question.answer'
                                _question_answer_code_ = question_answer.code
                                _question_answer_value_ = question_answer.value
                                _question_answer_sequence_ = question_answer.sequence

                                yaml_file.write('            %s:\n' % (_question_answer_code_))
                                yaml_file.write('                model: %s\n' % (_question_answer_model_))
                                yaml_file.write('                value: \'%s\'\n' % (_question_answer_value_))
                                yaml_file.write('                code: \'%s\'\n' % (_question_answer_code_))
                                yaml_file.write('                question_id: %s\n' % (_question_code_))
                                yaml_file.write('                sequence: %s\n' % (_question_answer_sequence_))

                            yaml_file.write('\n')

                        if export_xls:

                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_title_)
                            row_nr += 1
                            row = sheet.row(row_nr)
                            row.write(0, '[' + _question_code_ + ']')
                            row.write(4, _question_type_ + '_' + _question_matrix_subtype_)
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

                                _matrix_row_code_ = matrix_row.code
                                _matrix_row_value_ = matrix_row.value

                                row = sheet.row(row_nr)
                                row.write(0, '[' + _matrix_row_code_ + ']')
                                row.write(5, _matrix_row_value_)
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

                if export_xml:

                    xml_file.write('            <!-- %s -->\n' % (_page_title_))
                    xml_file.write('            <record model="%s" id="%s">\n' % (_page_model_, _page_code_))
                    xml_file.write('                <field name="title">%s</field>\n' % (_page_title_))
                    xml_file.write('                <field name="is_page" eval="%s"/>\n' % (_is_page_))
                    xml_file.write('                <field name="code">%s</field>\n' % (_page_code_))
                    xml_file.write('                <field name="parameter">%s</field>\n' % (_page_parameter_))
                    xml_file.write('                <field name="survey_id" ref="%s"/>\n' % (_survey_code_))
                    xml_file.write('                <field name="sequence" eval="%s"/>\n' % (_page_sequence_))
                    if _page_description_ is not False:
                        xml_file.write('                <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                       (_page_description_))
                    xml_file.write('            </record>' + '\n')
                    xml_file.write('\n')

                if export_yaml:

                    yaml_file.write('    %s:\n' % (_page_code_))
                    yaml_file.write('        model: %s\n' % (_page_model_))
                    yaml_file.write('        title: \'%s\'\n' % (_page_title_))
                    yaml_file.write('        is_page: %s\n' % (_is_page_))
                    yaml_file.write('        code: \'%s\'\n' % (_page_code_))
                    yaml_file.write('        parameter: \'%s\'\n' % (_page_parameter_))
                    yaml_file.write('        survey_id: %s\n' % (_survey_code_))
                    yaml_file.write('        sequence: %s\n' % (_page_sequence_))
                    if _page_description_ is not False:
                        yaml_file.write('        description: \'%s\'\n' % (_page_description_))
                    yaml_file.write('\n')

                if export_txt:

                    txt_file.write('    %s\n' % (_page_title_))
                    if _page_description_ is not False:
                        txt_file.write('        %s\n\n' % (_page_description_))
                    else:
                        txt_file.write('\n')

                if export_xls:

                    nonlocal row_nr

                    row = sheet.row(row_nr)
                    row.write(0, '[' + page.code + ']')
                    row.write(3, _page_title_)
                    # row_nr += 1
                    row_nr = row_nr + 1
                    row = sheet.row(row_nr)
                    row.write(0, '[' + page.code + ']')
                    row.write(3, _page_description_)
                    row_nr += 2

                for question in page.question_ids:

                    survey_question(question)

            if export_xml:

                xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
                xml_file.write('<odoo>\n')
                xml_file.write('    <data noupdate="1">\n')
                xml_file.write('\n')

                xml_file.write('        <!-- %s -->\n' % (_survey_title_))
                xml_file.write('        <record model="%s" id="%s">\n' % (_survey_model_, _survey_code_))
                xml_file.write('            <field name="title">%s</field>\n' % (_survey_title_))
                xml_file.write('            <field name="code">%s</field>\n' % (_survey_code_))
                xml_file.write('            <field name="state">%s</field>\n' % (_survey_state_))
                xml_file.write('            <field name="users_login_required" eval="%s"/>\n' % (_survey_users_login_required_))
                xml_file.write('            <field name="attempts_limit" eval="%s"/>\n' % (_survey_attempts_limit_))
                xml_file.write('            <field name="users_can_go_back" eval="%s"/>\n' % (_survey_users_can_go_back_))
                if _survey_description_ is not False:
                    xml_file.write('            <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                   (_survey_description_))
                xml_file.write('            <field name="questions_layout">%s</field>\n' % (_survey_questions_layout_))
                # xml_file.write('            <field name="phase_id" eval="%s"/>\n' % (self.phase_id))
                # xml_file.write('            <field name="ref_model" eval="%s"/>\n' % (self.ref_model))
                xml_file.write('            <field name="progression_mode">%s</field>\n' % (_survey_progression_mode_))
                xml_file.write('            <field name="is_time_limited" eval="%s"/>\n' % (_survey_is_time_limited_))
                xml_file.write('            <field name="questions_selection">%s</field>\n' % (_survey_questions_selection_))
                xml_file.write('        </record>\n')
                xml_file.write('\n')

            if export_yaml:

                yaml_file.write('%s:\n' % (self.code))
                yaml_file.write('    model: %s\n' % (_survey_model_))
                yaml_file.write('    title: \'%s\'\n' % (_survey_title_))
                yaml_file.write('    code: \'%s\'\n' % (_survey_code_))
                yaml_file.write('    state: \'%s\'\n' % (_survey_state_))
                yaml_file.write('    users_login_required: %s\n' % (_survey_users_login_required_))
                yaml_file.write('    attempts_limit: %s\n' % (_survey_attempts_limit_))
                yaml_file.write('    users_can_go_back: %s\n' % (_survey_users_can_go_back_))
                if _survey_description_ is not False:
                    yaml_file.write('    description: \'%s\'\n' % (_survey_description_))
                yaml_file.write('    questions_layout: \'%s\'\n' % (_survey_questions_layout_))
                yaml_file.write('    progression_mode: \'%s\'\n' % (_survey_progression_mode_))
                yaml_file.write('    is_time_limited: %s\n' % (_survey_is_time_limited_))
                yaml_file.write('    questions_selection: \'%s\'\n' % (_survey_questions_selection_))
                yaml_file.write('\n')

            if export_txt:

                txt_file.write('%s\n' % (_survey_title_))
                if _survey_description_ is not False:
                    txt_file.write('%s\n\n' % (_survey_description_))
                else:
                    txt_file.write('\n')

            if export_xls:

                nonlocal row_nr

                # _title_ = survey_reg.title
                # _description_ = survey_reg.description.replace('<p>', '').replace('</p>', '')

                sheet = book.add_sheet(_survey_code_)
                row = sheet.row(row_nr)
                row.write(0, '[' + _survey_code_ + ']')
                row_nr += 1

                row = sheet.row(row_nr)
                row.write(0, '[' + _survey_code_ + ']')
                row.write(2, _survey_title_)
                row_nr += 1
                row = sheet.row(row_nr)
                row.write(0, '[' + _survey_code_ + ']')
                row.write(2, _survey_description_)
                row_nr += 2

            pages = SurveyQuestion.search([
                ('survey_id', '=', self.id),
                ('is_page', '=', True),
            ])

            for page in pages:

                survey_page(page)

            if export_xml:

                xml_file.write('    </data>\n')
                xml_file.write('</odoo>\n')
                xml_file.close()

            if export_yaml:

                yaml_file.close()

            if export_xls:

                sheet.col(0).hidden = isHidden

                if file_format == 'preformatted':

                    for i in range(100):
                        sheet.col(i).width = 256 * 2

                    sheet.protect = True
                    sheet.password = password

                book.save(xls_filepath)

        survey()

        if export_yaml:
            yaml_file.close()

        if export_txt:
            txt_file.close()

        if export_xml:
            xml_file.close()

        if export_xls:
            pass

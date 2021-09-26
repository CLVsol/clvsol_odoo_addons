# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyExportXML(models.TransientModel):
    _description = 'Survey Export XML'
    _name = 'clv.survey.export_xml'

    def _default_survey_ids(self):
        return self._context.get('active_ids')
    survey_ids = fields.Many2many(
        comodel_name='survey.survey',
        relation='clv_survey_export_xml_rel',
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

    def do_survey_export_xml(self):
        self.ensure_one()

        SurveyQuestion = self.env['survey.question']

        for survey_reg in self.survey_ids:

            file_path = self.dir_path + '/' + self.file_name.replace('<code>', survey_reg.code)

            _logger.info(u'%s %s', '>>>>>', file_path)

            xml_file = open(file_path, "w")

            xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xml_file.write('<odoo>\n')
            xml_file.write('    <data noupdate="1">\n')
            xml_file.write('\n')

            _model_ = 'survey.survey'
            _state_ = 'open'
            xml_file.write('        <!-- %s -->\n' % (survey_reg.title))
            xml_file.write('        <record model="%s" id="%s">\n' % (_model_, survey_reg.code))
            xml_file.write('            <field name="title">%s</field>\n' % (survey_reg.title))
            xml_file.write('            <field name="code">%s</field>\n' % (survey_reg.code))
            xml_file.write('            <field name="state">%s</field>\n' % (_state_))
            xml_file.write('            <field name="users_login_required" eval="%s"/>\n' % (survey_reg.users_login_required))
            xml_file.write('            <field name="attempts_limit" eval="%s"/>\n' % (survey_reg.attempts_limit))
            xml_file.write('            <field name="users_can_go_back" eval="%s"/>\n' %
                           (survey_reg.users_can_go_back))
            if survey_reg.description is not False and survey_reg.description != '<p><br></p>':
                _description_ = survey_reg.description.replace('<p>', '').replace('</p>', '')
                xml_file.write('            <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' % (_description_))
            xml_file.write('            <field name="questions_layout">%s</field>\n' % (survey_reg.questions_layout))
            # xml_file.write('            <field name="phase_id" eval="%s"/>\n' % (survey_reg.phase_id))
            # xml_file.write('            <field name="ref_model" eval="%s"/>\n' % (survey_reg.ref_model))
            xml_file.write('            <field name="progression_mode">%s</field>\n' % (survey_reg.progression_mode))
            xml_file.write('            <field name="is_time_limited" eval="%s"/>\n' % (survey_reg.is_time_limited))
            xml_file.write('            <field name="questions_selection">%s</field>\n' % (survey_reg.questions_selection))
            xml_file.write('        </record>\n')
            xml_file.write('\n')

            pages = SurveyQuestion.search([
                ('survey_id', '=', survey_reg.id),
                ('is_page', '=', True),
            ])

            for page in pages:

                _title_ = page.title
                _model_ = 'survey.question'

                xml_file.write('            <!-- %s -->\n' % (_title_))
                xml_file.write('            <record model="%s" id="%s">\n' % (_model_, page.code))
                xml_file.write('                <field name="title">%s</field>\n' % (_title_))
                xml_file.write('                <field name="is_page" eval="%s"/>\n' % (page.is_page))
                xml_file.write('                <field name="code">%s</field>\n' % (page.code))
                xml_file.write('                <field name="parameter">%s</field>\n' % (page.parameter))
                xml_file.write('                <field name="survey_id" ref="%s"/>\n' % (survey_reg.code))
                xml_file.write('                <field name="sequence" eval="%s"/>\n' % (page.sequence))
                if page.description is not False and page.description != '<p><br></p>':
                    _description_ = page.description.replace('<p>', '').replace('</p>', '')
                    xml_file.write('                <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' % (_description_))
                xml_file.write('            </record>' + '\n')
                xml_file.write('\n')

                for question in page.question_ids:

                    question_type = question.question_type
                    _question_ = question.title
                    _model_ = 'survey.question'
                    if question.comments_message is not False:
                        _comments_message_ = question.comments_message
                    if question.comments_allowed is False:
                        _comments_message_ = ''

                    if question_type == 'char_box' or question_type == 'text_box' or question_type == 'datetime':

                        xml_file.write('                <!-- %s -->\n' % (_question_))
                        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, question.code))
                        xml_file.write('                    <field name="title">%s</field>\n' % (_question_))
                        xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (question.is_page))
                        xml_file.write('                    <field name="code">%s</field>\n' % (question.code))
                        if question.parameter:
                            xml_file.write('                    <field name="parameter">%s</field>\n' % (question.parameter))
                        xml_file.write('                    <field name="question_type">%s</field>\n' % (question_type))
                        xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (survey_reg.code))
                        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (question.sequence))
                        if question.description is not False and question.description != '<p><br></p>':
                            _description_ = question.description.replace('<p>', '').replace('</p>', '')
                            xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                           (_description_))
                        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                       (question.constr_mandatory))
                        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                       (question.constr_error_msg))
                        xml_file.write('                </record>\n')
                        xml_file.write('\n')

                    if question_type == 'simple_choice':

                        xml_file.write('                <!-- %s -->\n' % (_question_))
                        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, question.code))
                        xml_file.write('                    <field name="title">%s</field>\n' % (_question_))
                        xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (question.is_page))
                        xml_file.write('                    <field name="code">%s</field>\n' % (question.code))
                        if question.parameter:
                            xml_file.write('                    <field name="parameter">%s</field>\n' % (question.parameter))
                        xml_file.write('                    <field name="question_type">%s</field>\n' % (question_type))
                        xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (survey_reg.code))
                        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (question.sequence))
                        if question.description is not False and question.description != '<p><br></p>':
                            _description_ = question.description.replace('<p>', '').replace('</p>', '')
                            xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                           (_description_))
                        xml_file.write('                    <field name="column_nb">%s</field>\n' %
                                       (question.column_nb))
                        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                       (question.constr_mandatory))
                        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                       (question.constr_error_msg))
                        xml_file.write('                    <field name="comments_allowed">%s</field>\n' %
                                       (question.comments_allowed))
                        xml_file.write('                    <field name="comments_message">%s</field>\n' %
                                       (_comments_message_))
                        xml_file.write('                    <field name="comment_count_as_answer">%s</field>\n' %
                                       (question.comment_count_as_answer))
                        xml_file.write('                </record>\n')
                        xml_file.write('\n')

                        for question_answer in question.suggested_answer_ids:

                            _model_ = 'survey.question.answer'

                            xml_file.write(
                                '                    <record model="%s" id="%s">\n' % (_model_, question_answer.code)
                            )
                            xml_file.write('                        <field name="value">%s</field>\n' %
                                           (question_answer.value))
                            xml_file.write('                        <field name="code">%s</field>\n' % (question_answer.code))
                            xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                           (question.code))
                            xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                           (question_answer.sequence))
                            xml_file.write('                    </record>\n')
                            xml_file.write('\n')

                    if question_type == 'multiple_choice':

                        xml_file.write('                <!-- %s -->\n' % (_question_))
                        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, question.code))
                        xml_file.write('                    <field name="title">%s</field>\n' % (_question_))
                        xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (question.is_page))
                        xml_file.write('                    <field name="code">%s</field>\n' % (question.code))
                        if question.parameter:
                            xml_file.write('                    <field name="parameter">%s</field>\n' % (question.parameter))
                        xml_file.write('                    <field name="question_type">%s</field>\n' % (question_type))
                        xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (survey_reg.code))
                        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (question.sequence))
                        if question.description is not False and question.description != '<p><br></p>':
                            _description_ = question.description.replace('<p>', '').replace('</p>', '')
                            xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                           (_description_))
                        xml_file.write('                    <field name="column_nb">%s</field>\n' %
                                       (question.column_nb))
                        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                       (question.constr_mandatory))
                        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                       (question.constr_error_msg))
                        xml_file.write('                    <field name="comments_allowed">%s</field>\n' %
                                       (question.comments_allowed))
                        xml_file.write('                    <field name="comments_message">%s</field>\n' %
                                       (_comments_message_))
                        xml_file.write('                    <field name="comment_count_as_answer">%s</field>\n' %
                                       (question.comment_count_as_answer))
                        xml_file.write('                </record>\n')
                        xml_file.write('\n')

                        for question_answer in question.suggested_answer_ids:

                            _model_ = 'survey.question.answer'

                            xml_file.write(
                                '                    <record model="%s" id="%s">\n' % (_model_, question_answer.code)
                            )
                            xml_file.write('                        <field name="value">%s</field>\n' %
                                           (question_answer.value))
                            xml_file.write('                        <field name="code">%s</field>\n' % (question_answer.code))
                            xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                           (question.code))
                            xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                           (question_answer.sequence))
                            xml_file.write('                    </record>\n')
                            xml_file.write('\n')

                    if question_type == 'matrix':

                        xml_file.write('                <!-- %s -->\n' % (_question_))
                        xml_file.write('                <record model="%s" id="%s">\n' % (_model_, question.code))
                        xml_file.write('                    <field name="title">%s</field>\n' % (_question_))
                        xml_file.write('                    <field name="is_page" eval="%s"/>\n' % (question.is_page))
                        xml_file.write('                    <field name="code">%s</field>\n' % (question.code))
                        if question.parameter:
                            xml_file.write('                    <field name="parameter">%s</field>\n' % (question.parameter))
                        xml_file.write('                    <field name="question_type">%s</field>\n' % (question_type))
                        xml_file.write('                    <field name="matrix_subtype">%s</field>\n' %
                                       (question.matrix_subtype))
                        xml_file.write('                    <field name="survey_id" ref="%s"/>\n' % (survey_reg.code))
                        xml_file.write('                    <field name="sequence" eval="%s"/>\n' % (question.sequence))
                        if question.description is not False and question.description != '<p><br></p>':
                            _description_ = question.description.replace('<p>', '').replace('</p>', '')
                            xml_file.write('                    <field name="description">&lt;p&gt;%s&lt;/p&gt;</field>\n' %
                                           (_description_))
                        xml_file.write('                    <field name="constr_mandatory">%s</field>\n' %
                                       (question.constr_mandatory))
                        xml_file.write('                    <field name="constr_error_msg">%s</field>\n' %
                                       (question.constr_error_msg))
                        xml_file.write('                </record>\n')
                        xml_file.write('\n')

                        for matrix_row in question.matrix_row_ids:

                            _model_ = 'survey.question.answer'

                            xml_file.write(
                                '                    <record model="%s" id="%s">\n' % (_model_, matrix_row.code)
                            )
                            xml_file.write('                        <field name="value">%s</field>\n' %
                                           (matrix_row.value))
                            xml_file.write('                        <field name="code">%s</field>\n' % (matrix_row.code))
                            xml_file.write('                        <field name="matrix_question_id" ref="%s"/>\n' %
                                           (question.code))
                            xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                           (matrix_row.sequence))
                            xml_file.write('                    </record>\n')
                            xml_file.write('\n')

                        for question_answer in question.suggested_answer_ids:

                            _model_ = 'survey.question.answer'

                            xml_file.write(
                                '                    <record model="%s" id="%s">\n' % (_model_, question_answer.code)
                            )
                            xml_file.write('                        <field name="value">%s</field>\n' %
                                           (question_answer.value))
                            xml_file.write('                        <field name="code">%s</field>\n' % (question_answer.code))
                            xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                           (question.code))
                            xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                           (question_answer.sequence))
                            xml_file.write('                    </record>\n')
                            xml_file.write('\n')

            xml_file.write('    </data>\n')
            xml_file.write('</odoo>\n')

            xml_file.close()

        return True

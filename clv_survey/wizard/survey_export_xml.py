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

    def do_survey_export_xml(self):
        self.ensure_one()

        SurveyQuestion = self.env['survey.question']

        for survey_reg in self.survey_ids:

            xml_file_path = self.dir_path + '/' + self.file_name.replace('<code>', survey_reg.code)
            yaml_file_path = xml_file_path.replace('.xml', '.yaml')

            if self.export_xml is True:

                _logger.info(u'%s %s', '>>>>>', xml_file_path)

                xml_file = open(xml_file_path, "w")

            if self.export_yaml is True:

                _logger.info(u'%s %s', '>>>>>', yaml_file_path)

                yaml_file = open(yaml_file_path, "w")

            _survey_title_ = survey_reg.title
            _survey_model_ = 'survey.survey'
            _survey_state_ = survey_reg.state
            _survey_code_ = survey_reg.code
            _survey_users_login_required_ = survey_reg.users_login_required
            _survey_attempts_limit_ = survey_reg.attempts_limit
            _survey_users_can_go_back_ = survey_reg.users_can_go_back
            _survey_description_ = False
            if survey_reg.description is not False and survey_reg.description != '<p><br></p>':
                _survey_description_ = survey_reg.description.replace('<p>', '').replace('</p>', '')
            _survey_questions_layout_ = survey_reg.questions_layout
            _survey_progression_mode_ = survey_reg.progression_mode
            _survey_is_time_limited_ = survey_reg.is_time_limited
            _survey_questions_selection_ = survey_reg.questions_selection

            if self.export_xml is True:

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
                # xml_file.write('            <field name="phase_id" eval="%s"/>\n' % (survey_reg.phase_id))
                # xml_file.write('            <field name="ref_model" eval="%s"/>\n' % (survey_reg.ref_model))
                xml_file.write('            <field name="progression_mode">%s</field>\n' % (_survey_progression_mode_))
                xml_file.write('            <field name="is_time_limited" eval="%s"/>\n' % (_survey_is_time_limited_))
                xml_file.write('            <field name="questions_selection">%s</field>\n' % (_survey_questions_selection_))
                xml_file.write('        </record>\n')
                xml_file.write('\n')

            if self.export_yaml is True:

                yaml_file.write('%s:\n' % (survey_reg.code))
                yaml_file.write('    model: %s\n' % (_survey_model_))
                yaml_file.write('    title: \'%s\'\n' % (_survey_title_))
                yaml_file.write('    code: \'%s\'\n' % (_survey_code_))
                yaml_file.write('    state: \'%s\'\n' % (_survey_state_))
                yaml_file.write('    users_login_required: %s\n' % (_survey_users_login_required_))
                yaml_file.write('    attempts_limit: %s\n' % (_survey_attempts_limit_))
                yaml_file.write('    users_can_go_back: %s\n' % (_survey_users_can_go_back_))
                if _survey_description_ is not False:
                    _survey_description_ = survey_reg.description.replace('<p>', '').replace('</p>', '')
                    yaml_file.write('    description: \'%s\'\n' % (_survey_description_))
                yaml_file.write('    questions_layout: \'%s\'\n' % (_survey_questions_layout_))
                yaml_file.write('    progression_mode: \'%s\'\n' % (_survey_progression_mode_))
                yaml_file.write('    is_time_limited: %s\n' % (_survey_is_time_limited_))
                yaml_file.write('    questions_selection: \'%s\'\n' % (_survey_questions_selection_))
                yaml_file.write('\n')

            pages = SurveyQuestion.search([
                ('survey_id', '=', survey_reg.id),
                ('is_page', '=', True),
            ])

            for page in pages:

                _page_title_ = page.title
                _page_model_ = 'survey.question'
                _page_code_ = page.code
                _is_page_ = page.is_page
                _page_parameter_ = page.parameter
                _page_sequence_ = page.sequence
                if page.description is not False and page.description != '<p><br></p>':
                    _page_description_ = page.description.replace('<p>', '').replace('</p>', '')

                if self.export_xml is True:

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

                if self.export_yaml is True:

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

                for question in page.question_ids:

                    _question_type_ = question.question_type
                    _question_title_ = question.title
                    _question_model_ = 'survey.question'
                    if question.comments_message is not False:
                        _comments_message_ = question.comments_message
                    if question.comments_allowed is False:
                        _comments_message_ = ''

                    _is_page_ = question.is_page
                    _question_code_ = question.code
                    _question_parameter_ = question.parameter
                    _question_sequence_ = question.sequence
                    if question.description is not False:
                        _question_description_ = question.description.replace('<p>', '').replace('</p>', '')
                    _question_constr_mandatory_ = question.constr_mandatory
                    _question_constr_error_msg_ = question.constr_error_msg
                    _question_comment_count_as_answer_ = question.comment_count_as_answer
                    _question_column_nb_ = question.column_nb
                    _question_matrix_subtype_ = question.matrix_subtype

                    if _question_type_ == 'char_box' or _question_type_ == 'text_box' or _question_type_ == 'datetime':

                        if self.export_xml is True:

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

                        if self.export_yaml is True:

                            yaml_file.write('        %s:\n' % (_question_code_))
                            yaml_file.write('            model: %s\n' % (_question_model_))
                            yaml_file.write('            title: \'%s\'\n' % (_question_title_))
                            yaml_file.write('            is_page: %s\n' % (_is_page_))
                            yaml_file.write('            code: \'%s\'\n' % (_question_code_))
                            if question.parameter:
                                yaml_file.write('            parameter: \'%s\'\n' % (_question_parameter_))
                            yaml_file.write('            question_type: \'%s\'\n' % (question.question_type))
                            yaml_file.write('            survey_id: %s\n' % (_survey_code_))
                            yaml_file.write('            sequence: %s\n' % (page.sequence))
                            if _question_description_ is not False:
                                yaml_file.write('            description: \'%s\'\n' % (_question_description_))
                            yaml_file.write('            constr_mandatory: %s\n' % (_question_constr_mandatory_))
                            yaml_file.write('            constr_error_msg: \'%s\'\n' % (_question_constr_error_msg_))
                            yaml_file.write('\n')

                    if _question_type_ == 'simple_choice':

                        if self.export_xml is True:

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
                                           (_comments_message_))
                            xml_file.write('                    <field name="comment_count_as_answer">%s</field>\n' %
                                           (_question_comment_count_as_answer_))
                            xml_file.write('                </record>\n')
                            xml_file.write('\n')

                        if self.export_yaml is True:

                            pass

                        for question_answer in question.suggested_answer_ids:

                            _model_ = 'survey.question.answer'

                            if self.export_xml is True:

                                xml_file.write(
                                    '                    <record model="%s" id="%s">\n' % (_model_, question_answer.code)
                                )
                                xml_file.write('                        <field name="value">%s</field>\n' %
                                               (question_answer.value))
                                xml_file.write('                        <field name="code">%s</field>\n' %
                                               (question_answer.code))
                                xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                               (_question_code_))
                                xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                               (question_answer.sequence))
                                xml_file.write('                    </record>\n')
                                xml_file.write('\n')

                            if self.export_yaml is True:

                                pass

                    if _question_type_ == 'multiple_choice':

                        if self.export_xml is True:

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
                                           (_comments_message_))
                            xml_file.write('                    <field name="comment_count_as_answer">%s</field>\n' %
                                           (_question_comment_count_as_answer_))
                            xml_file.write('                </record>\n')
                            xml_file.write('\n')

                        if self.export_yaml is True:

                            pass

                        for question_answer in question.suggested_answer_ids:

                            _model_ = 'survey.question.answer'

                            if self.export_xml is True:

                                xml_file.write(
                                    '                    <record model="%s" id="%s">\n' % (_model_, question_answer.code)
                                )
                                xml_file.write('                        <field name="value">%s</field>\n' %
                                               (question_answer.value))
                                xml_file.write('                        <field name="code">%s</field>\n' %
                                               (question_answer.code))
                                xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                               (_question_code_))
                                xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                               (question_answer.sequence))
                                xml_file.write('                    </record>\n')
                                xml_file.write('\n')

                            if self.export_yaml is True:

                                pass

                    if _question_type_ == 'matrix':

                        if self.export_xml is True:

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

                        if self.export_yaml is True:

                            pass

                        for matrix_row in question.matrix_row_ids:

                            _model_ = 'survey.question.answer'

                            if self.export_xml is True:

                                xml_file.write(
                                    '                    <record model="%s" id="%s">\n' % (_model_, matrix_row.code)
                                )
                                xml_file.write('                        <field name="value">%s</field>\n' %
                                               (matrix_row.value))
                                xml_file.write('                        <field name="code">%s</field>\n' % (matrix_row.code))
                                xml_file.write('                        <field name="matrix_question_titleid" ref="%s"/>\n' %
                                               (_question_code_))
                                xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                               (matrix_row.sequence))
                                xml_file.write('                    </record>\n')
                                xml_file.write('\n')

                            if self.export_yaml is True:

                                pass

                        for question_answer in question.suggested_answer_ids:

                            _model_ = 'survey.question.answer'

                            if self.export_xml is True:

                                xml_file.write(
                                    '                    <record model="%s" id="%s">\n' % (_model_, question_answer.code)
                                )
                                xml_file.write('                        <field name="value">%s</field>\n' %
                                               (question_answer.value))
                                xml_file.write('                        <field name="code">%s</field>\n' %
                                               (question_answer.code))
                                xml_file.write('                        <field name="question_id" ref="%s"/>\n' %
                                               (_question_code_))
                                xml_file.write('                        <field name="sequence" eval="%s"/>\n' %
                                               (question_answer.sequence))
                                xml_file.write('                    </record>\n')
                                xml_file.write('\n')

                            if self.export_yaml is True:

                                pass

            if self.export_xml is True:

                xml_file.write('    </data>\n')
                xml_file.write('</odoo>\n')

                xml_file.close()

            if self.export_yaml is True:

                xml_file.close()

        return True

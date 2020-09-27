# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveyDuplicate(models.TransientModel):
    _description = 'Survey Duplicate'
    _name = 'survey.survey.duplicate'

    survey_ids = fields.Many2many(
        comodel_name='survey.survey',
        relation='survey_survey_duplicate_rel',
        string='Surveys'
    )

    new_title = fields.Char(
        string='New Survey Title',
        required=True
    )

    new_description = fields.Char(
        string='New Survey Description',
        required=True
    )

    new_code = fields.Char(
        string='New Survey Code',
        required=True
    )

    new_access_token = fields.Char(
        string='New Access Token',
        required=True
    )

    # phase_id = fields.Many2one(
    #     comodel_name='clv.phase',
    #     string='Phase'
    # )

    @api.model
    def default_get(self, field_names):

        defaults = super(SurveyDuplicate, self).default_get(field_names)

        defaults['survey_ids'] = self.env.context['active_ids']

        Survey = self.env['survey.survey']
        survey_id = self._context.get('active_id')
        survey = Survey.search([
            ('id', '=', survey_id),
        ])
        defaults['new_title'] = survey.title
        defaults['new_description'] = survey.description
        defaults['new_code'] = survey.code
        defaults['new_access_token'] = survey.access_token

        # phase_id = int(self.env['ir.config_parameter'].sudo().get_param(
        #     'clv.global_settings.current_phase_id', '').strip())
        # defaults['phase_id'] = phase_id

        return defaults

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

    def do_survey_duplicate(self):
        self.ensure_one()

        SurveySurvey = self.env['survey.survey']
        SurveyQuestion = self.env['survey.question']
        SurveyLabel = self.env['survey.label']

        for survey in self.survey_ids:

            _logger.info(u'%s %s %s %s', '>>>>>', survey.code, survey.title, survey.description)
            _logger.info(u'%s %s %s %s', '>>>>>>>>>>', self.new_code, self.new_title, self.new_description)

            values = {
                'title': self.new_title,
                'code': self.new_code,
                'access_token': self.new_access_token,
                'users_login_required': survey.users_login_required,
                'attempts_limit': survey.attempts_limit,
                'users_can_go_back': survey.users_can_go_back,
                'description': self.new_description,
                'thank_you_message': survey.thank_you_message,
                'questions_layout': survey.questions_layout,
                # 'auth_required': survey.auth_required,
                # 'stage_id': survey.stage_id.id,
                # 'phase_id': self.phase_id.id,
            }
            new_survey = SurveySurvey.create(values)

            pages = SurveyQuestion.search([
                ('survey_id', '=', survey.id),
                ('is_page', '=', True),
            ])

            for page in pages:

                new_page_code = page.code.replace(survey.code, self.new_code)

                _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>>', new_page_code, page.title)

                values = {
                    'title': page.title,
                    'is_page': page.is_page,
                    'page_id': page.page_id,
                    'code': new_page_code,
                    'parameter': page.parameter,
                    'question_type': page.question_type,
                    'survey_id': new_survey.id,
                    'sequence': page.sequence,
                    'description': page.description,
                    'constr_mandatory': page.constr_mandatory,
                    'constr_error_msg': page.constr_error_msg,
                    'display_mode': page.display_mode,
                    'column_nb': page.column_nb,
                    'comments_allowed': page.comments_allowed,
                    'comments_message': page.comments_message,
                    'comment_count_as_answer': page.comment_count_as_answer,
                    'matrix_subtype': page.matrix_subtype,
                }
                new_page = SurveyQuestion.create(values)

                # questions = SurveyQuestion.search([
                #     ('survey_id', '=', survey.id),
                #     ('page_id', '=', page.id),
                #     ('is_page', '=', False),
                # ])

                for question in page.question_ids:

                    new_question_code = question.code.replace(survey.code, self.new_code)

                    _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>>>>>>>', new_question_code, question.question)

                    values = {
                        'title': question.title,
                        'is_page': question.is_page,
                        'page_id': new_page.id,
                        'code': new_question_code,
                        'parameter': question.parameter,
                        'question_type': question.question_type,
                        'survey_id': new_survey.id,
                        'sequence': question.sequence,
                        'description': question.description,
                        'constr_mandatory': question.constr_mandatory,
                        'constr_error_msg': question.constr_error_msg,
                        'display_mode': question.display_mode,
                        'column_nb': question.column_nb,
                        'comments_allowed': question.comments_allowed,
                        'comments_message': question.comments_message,
                        'comment_count_as_answer': question.comment_count_as_answer,
                        'matrix_subtype': question.matrix_subtype,
                    }
                    new_question = SurveyQuestion.create(values)

                    for label in question.labels_ids:

                        new_label_code = label.code.replace(survey.code, self.new_code)

                        _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>>>>>>>>>>>>', new_label_code, label.value)

                        values = {
                            'value': label.value,
                            'code': new_label_code,
                            'question_id': new_question.id,
                            'sequence': label.sequence,
                        }
                        SurveyLabel.create(values)

                    for label in question.labels_ids_2:

                        new_label_code = label.code.replace(survey.code, self.new_code)

                        _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>>>>>>>>>>>>', new_label_code, label.value)

                        values = {
                            'value': label.value,
                            'code': new_label_code,
                            'question_id_2': new_question.id,
                            'sequence': label.sequence,
                        }
                        SurveyLabel.create(values)

        return True

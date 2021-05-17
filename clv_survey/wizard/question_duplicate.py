# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class QuestionDuplicate(models.TransientModel):
    _description = 'Question Duplicate'
    _name = 'survey.question.duplicate'

    def _default_question_ids(self):
        return self._context.get('active_ids')
    question_ids = fields.Many2many(
        comodel_name='survey.question',
        relation='survey_question_duplicate_rel',
        string='Questions',
        default=_default_question_ids
    )

    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey'
    )

    @api.model
    def default_get(self, field_names):

        defaults = super(QuestionDuplicate, self).default_get(field_names)

        # defaults['question_ids'] = self.env.context['active_ids']

        Question = self.env['survey.question']
        question_id = self._context.get('active_id')
        question = Question.search([
            ('id', '=', question_id),
        ])
        defaults['survey_id'] = question.survey_id.id

        return defaults

    def _create_question(self, dest_survey, new_page, question, sequence):

        _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>', question.title)

        SurveyQuestion = self.env['survey.question']
        SurveyQuestionAnswer = self.env['survey.question.answer']

        values = {
            'title': question.title,
            'is_page': question.is_page,
            'page_id': new_page.id,
            'parameter': question.parameter,
            'question_type': question.question_type,
            'survey_id': dest_survey.id,
            'sequence': sequence,
            'description': question.description,
            'constr_mandatory': question.constr_mandatory,
            'constr_error_msg': question.constr_error_msg,
            # 'display_mode': question.display_mode,
            'column_nb': question.column_nb,
            'comments_allowed': question.comments_allowed,
            'comments_message': question.comments_message,
            'comment_count_as_answer': question.comment_count_as_answer,
            'matrix_subtype': question.matrix_subtype,
        }
        new_question = SurveyQuestion.create(values)

        for suggested_answer in question.suggested_answer_ids:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>>>>>>', suggested_answer.value)

            values = {
                'value': suggested_answer.value,
                'question_id': new_question.id,
                'sequence': suggested_answer.sequence,
            }
            SurveyQuestionAnswer.create(values)

        for matrix_row in question.matrix_row_ids:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>>>>>>', matrix_row.value)

            values = {
                'value': matrix_row.value,
                'matrix_question_id_2': new_question.id,
                'sequence': matrix_row.sequence,
            }
            SurveyQuestionAnswer.create(values)

        return new_question

    def do_question_duplicate(self):
        self.ensure_one()

        SurveyQuestion = self.env['survey.question']

        for ref_question in self.question_ids:

            _logger.info(u'%s %s %s %s', '>>>>>', ref_question.code, ref_question.title, ref_question.description)
            _logger.info(u'%s %s %s', '>>>>>>>>>>', ref_question.survey_id.title, self.survey_id.title)

            if ref_question.is_page:

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', ref_question.title)

                question_ids = ref_question.question_ids

                sequence = 0
                for question in self.survey_id.question_ids:
                    if question.sequence > sequence:
                        sequence = question.sequence

                values = {
                    'title': ref_question.title,
                    'is_page': ref_question.is_page,
                    'page_id': ref_question.page_id,
                    'parameter': ref_question.parameter,
                    'question_type': ref_question.question_type,
                    'survey_id': self.survey_id.id,
                    'sequence': sequence,
                    'description': ref_question.description,
                    'constr_mandatory': ref_question.constr_mandatory,
                    'constr_error_msg': ref_question.constr_error_msg,
                    # 'display_mode': ref_question.display_mode,
                    'column_nb': ref_question.column_nb,
                    'comments_allowed': ref_question.comments_allowed,
                    'comments_message': ref_question.comments_message,
                    'comment_count_as_answer': ref_question.comment_count_as_answer,
                    'matrix_subtype': ref_question.matrix_subtype,
                }
                new_page = SurveyQuestion.create(values)

                for question in question_ids:

                    self._create_question(self.survey_id, new_page, question, sequence)

            else:

                self._create_question(self.survey_id, ref_question.page_id, ref_question, ref_question.sequence)

        return True

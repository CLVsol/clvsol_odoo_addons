# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyCodeRenew(models.TransientModel):
    _description = 'Survey Code Renew'
    _name = 'clv.survey.code_renew'

    def _default_survey_ids(self):
        return self._context.get('active_ids')
    survey_ids = fields.Many2many(
        comodel_name='survey.survey',
        relation='clv_survey_code_renew_rel',
        string='Surveys',
        default=_default_survey_ids
    )

    def do_survey_code_renew(self):
        self.ensure_one()

        SurveyQuestion = self.env['survey.question']

        for survey in self.survey_ids:

            _logger.info(u'%s %s', '>>>>>', survey.title)
            _logger.info(u'%s %s', '>>>>>', survey.code)

            new_survey_code = 'x' + survey.code

            pages = SurveyQuestion.search([
                ('survey_id', '=', survey.id),
                ('is_page', '=', True),
            ])

            new_page_sequence = 0
            for page in pages:

                new_page_sequence += 10000
                if new_page_sequence < 100000:
                    new_page_code = new_survey_code + '_0' + str(int(new_page_sequence / 10000))
                else:
                    new_page_code = new_survey_code + '_' + str(int(new_page_sequence / 10000))

                _logger.info(
                    u'%s %s: %s, %s: %s',
                    '>>>>>>>>>>', page.code, page.sequence, new_page_code[1:], new_page_sequence
                )

                new_question_sequence = new_page_sequence
                for question in page.question_ids:

                    question_type = question.question_type

                    new_question_sequence += 10
                    if (new_question_sequence - new_page_sequence) < 100:
                        new_question_code = \
                            new_page_code + '_0' + str(int((new_question_sequence - new_page_sequence) / 10))
                    else:
                        new_question_code = \
                            new_page_code + '_' + str(int((new_question_sequence - new_page_sequence) / 10))

                    _logger.info(
                        u'%s %s: %s, %s: %s',
                        '>>>>>>>>>>>>>>>',
                        question.code, question.sequence, new_question_code[1:], new_question_sequence
                    )

                    if question_type == 'free_text' or question_type == 'textbox' or question_type == 'datetime':

                        pass

                    if question_type == 'simple_choice':

                        new_label_sequence = 0
                        for label in question.labels_ids:

                            new_label_sequence += 10
                            if new_label_sequence < 100:
                                new_label_code = new_question_code + '_0' + str(int(new_label_sequence / 10))
                            else:
                                new_label_code = new_question_code + '_' + str(int(new_label_sequence / 10))

                            _logger.info(
                                u'%s %s: %s, %s: %s',
                                '>>>>>>>>>>>>>>>>>>>>',
                                label.code, label.sequence, new_label_code[1:], new_label_sequence
                            )

                            label.sequence = new_label_sequence
                            label.code = new_label_code

                    if question_type == 'multiple_choice':

                        new_label_sequence = 0
                        for label in question.labels_ids:

                            new_label_sequence += 10
                            if new_label_sequence < 100:
                                new_label_code = new_question_code + '_0' + str(int(new_label_sequence / 10))
                            else:
                                new_label_code = new_question_code + '_' + str(int(new_label_sequence / 10))

                            _logger.info(
                                u'%s %s: %s, %s: %s',
                                '>>>>>>>>>>>>>>>>>>>>',
                                label.code, label.sequence, new_label_code[1:], new_label_sequence
                            )

                            label.sequence = new_label_sequence
                            label.code = new_label_code

                    if question_type == 'matrix':

                        new_label_sequence = 0
                        for label in question.labels_ids_2:

                            new_label_sequence += 10
                            if new_label_sequence < 100:
                                new_label_code = new_question_code + '_0' + str(int(new_label_sequence / 10))
                            else:
                                new_label_code = new_question_code + '_' + str(int(new_label_sequence / 10))

                            _logger.info(
                                u'%s %s: %s, %s: %s',
                                '>>>>>>>>>>>>>>>>>>>>',
                                label.code, label.sequence, new_label_code[1:], new_label_sequence
                            )

                            label.sequence = new_label_sequence
                            label.code = new_label_code

                        for label in question.labels_ids:

                            new_label_sequence += 10
                            if new_label_sequence < 100:
                                new_label_code = new_question_code + '_0' + str(int(new_label_sequence / 10))
                            else:
                                new_label_code = new_question_code + '_' + str(int(new_label_sequence / 10))

                            _logger.info(
                                u'%s %s: %s, %s: %s',
                                '>>>>>>>>>>>>>>>>>>>>',
                                label.code, label.sequence, new_label_code[1:], new_label_sequence
                            )

                            label.sequence = new_label_sequence
                            label.code = new_label_code

                    question.sequence = new_question_sequence
                    question.code = new_question_code

                page.sequence = new_page_sequence
                page.code = new_page_code

            self.env.cr.commit()

            pages = SurveyQuestion.search([
                ('survey_id', '=', survey.id),
                ('is_page', '=', True),
            ])

            for page in pages:
                _logger.info(u'%s %s', '>>>>> (page.code[1:])', page.code[1:])
                page.code = page.code[1:]
                for question in page.question_ids:
                    _logger.info(u'%s %s', '>>>>> (question.code[1:])', question.code[1:])
                    question.code = question.code[1:]
                    for label in question.labels_ids_2:
                        _logger.info(u'%s %s', '>>>>> (label.code[1:])', label.code[1:])
                        label.code = label.code[1:]
                    for label in question.labels_ids:
                        _logger.info(u'%s %s', '>>>>> (label.code[1:])', label.code[1:])
                        label.code = label.code[1:]

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class LabTestResultSetSurveyUserInput(models.TransientModel):
    _description = 'Lab Test Result Set Survey User Input'
    _name = 'clv.lab_test.result.set_survey_user_input'

    @api.model
    def referenceable_models(self):
        return [(ref.model, ref.name) for ref in self.env['clv.referenceable.model'].search([
            ('base_model', '=', self._name),
        ])]

    def _default_lab_test_result_id(self):
        return self._context.get('active_id')
    lab_test_result_id = fields.Many2one(
        comodel_name='clv.lab_test.result',
        string='Lab Test Result',
        readonly=True,
        default=_default_lab_test_result_id
    )

    def _default_lab_test_type_id(self):
        return self.env['clv.lab_test.result'].browse(self._context.get('active_id')).lab_test_type_id
    lab_test_type_id = fields.Many2one(
        comodel_name='clv.lab_test.type',
        string='Lab Test Result Type',
        readonly=True,
        default=_default_lab_test_type_id
    )

    def _default_reference(self):
        reference = self.env['clv.lab_test.result'].browse(self._context.get('active_id')).ref_id
        if reference:
            ref_name = reference.name
            ref_code = reference.code
            return ref_name + ' [' + ref_code + ']'
        else:
            return False
    reference = fields.Char(
        string='Refers to',
        readonly=True,
        default=_default_reference
    )

    def do_lab_test_result_set_survey_user_input(self):
        self.ensure_one()

        lab_test_result = self.env['clv.lab_test.result'].browse(self._context.get('active_id'))

        _logger.info(u'%s %s', '>>>>>', self.lab_test_result_id.code)

        SurveyQuestion = self.env['survey.question']
        SurveyUserInput = self.env['survey.user_input']
        SurveyUserInputLine = self.env['survey.user_input.line']
        LabTestResultTypeParameter = self.env['clv.lab_test.type.parameter']

        if lab_test_result.survey_user_input_id.id is False:

            values = {
                # 'token': lab_test_result.code.replace('.', '-'),
                'survey_id': lab_test_result.survey_id.id,
                'ref_id': lab_test_result._name + ',' + str(lab_test_result.id),
            }

            new_user_input = SurveyUserInput.create(values)

            lab_test_result.survey_user_input_id = new_user_input.id

            questions = SurveyQuestion.search([
                ('survey_id', '=', lab_test_result.survey_id.id),
                ('is_page', '=', False),
            ])

            m2m_list = []
            for question in questions:
                m2m_list.append((4, question.id))
            new_user_input.predefined_question_ids = m2m_list

            lab_test_result_type_parameters = LabTestResultTypeParameter.search([
                ('lab_test_type_id', '=', lab_test_result.lab_test_type_id.id),
            ])

            for lab_test_result_type_parameter in lab_test_result_type_parameters:

                question = SurveyQuestion.search([
                    ('code', '=', lab_test_result_type_parameter.criterion_code),
                ])
                values = {
                    'user_input_id': new_user_input.id,
                    'survey_id': lab_test_result.survey_id.id,
                    'question_id': question.id,
                    'answer_type': lab_test_result_type_parameter.criterion_type,
                    'value_char_box': eval('lab_test_result.' + lab_test_result_type_parameter.name),
                }
                SurveyUserInputLine.create(values)

            _logger.info(u'%s %s', '>>>>>', new_user_input)

        return True

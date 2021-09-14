# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from werkzeug import urls
import re

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def format_code(code):
    code = re.sub("\D", "", code)
    code_len = len(code) - 2
    while len(code) < 16:
        code = '0' + code
    code_str = "%s.%s.%s.%s.%s-%s" % (str(code[0]) + str(code[1]),
                                      str(code[2]) + str(code[3]) + str(code[4]),
                                      str(code[5]) + str(code[6]) + str(code[7]),
                                      str(code[8]) + str(code[9]) + str(code[10]),
                                      str(code[11]) + str(code[12]) + str(code[13]),
                                      str(code[14]) + str(code[15]))
    if code_len <= 3:
        code_form = code_str[18 - code_len:21]
    elif code_len > 3 and code_len <= 6:
        code_form = code_str[17 - code_len:21]
    elif code_len > 6 and code_len <= 9:
        code_form = code_str[16 - code_len:21]
    elif code_len > 9 and code_len <= 12:
        code_form = code_str[15 - code_len:21]
    elif code_len > 12 and code_len <= 14:
        code_form = code_str[14 - code_len:21]
    return code_form


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    _rec_name = 'access_token'

    survey_url = fields.Char(
        string='Survey URL',
        compute="_compute_survey_url"
    )

    def _compute_survey_url(self):

        base_url = '/' if self.env.context.get('relative_url') else \
                   self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for user_input in self:
            # user_input.survey_url = \
            #     urls.url_join(base_url, "survey/fill/%s/%s" % (slug(user_input.survey_id), user_input.token))
            user_input.survey_url = \
                urls.url_join(
                    base_url, "survey/%s/%s" % (user_input.survey_id.access_token, user_input.access_token))

    def get_value(self, question_code):

        SurveyQuestion = self.env['survey.question']
        SurveyQuestionAnswer = self.env['survey.question.answer']
        SurveyUserInput = self.env['survey.user_input.line']

        survey_question_search = SurveyQuestion.search([
            ('code', '=', question_code[:11]),
        ])
        if question_code[:11] == question_code:
            survey_user_input_line_search = SurveyUserInput.search([
                ('user_input_id', '=', self.id),
                ('question_id', '=', survey_question_search.id),
            ])
        else:
            survey_question_answer_search = SurveyQuestionAnswer.search([
                ('code', '=', question_code),
            ])
            survey_user_input_line_search = SurveyUserInput.search([
                ('user_input_id', '=', self.id),
                ('question_id', '=', survey_question_search.id),
                ('suggested_answer_id', '=', survey_question_answer_search.id),
            ])

        value = False

        if survey_question_search.question_type == 'char_box':
            value = survey_user_input_line_search.value_char_box

        if survey_question_search.question_type == 'date':
            value = survey_user_input_line_search.value_date

        if survey_question_search.question_type == 'simple_choice':
            value = ''
            if question_code[11:13] == '_C':
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if survey_user_input_line_reg.value_char_box is not False:
                        value = survey_user_input_line_reg.value_char_box
            else:
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if value == '':
                        value = survey_user_input_line_reg.suggested_answer_id.value
                    else:
                        if survey_user_input_line_reg.suggested_answer_id.value is not False:
                            value = value + '; ' + survey_user_input_line_reg.suggested_answer_id.value
                        # else:
                        #     value = value + '; False'
                # value = survey_user_input_line_search.suggested_answer_id.value

        if survey_question_search.question_type == 'multiple_choice':
            value = ''
            if question_code[11:13] == '_C':
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if survey_user_input_line_reg.value_char_box is not False:
                        value = survey_user_input_line_reg.value_char_box
            else:
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if value == '':
                        value = survey_user_input_line_reg.suggested_answer_id.value
                    else:
                        if survey_user_input_line_reg.suggested_answer_id.value is not False:
                            value = value + '; ' + survey_user_input_line_reg.suggested_answer_id.value
                        # else:
                        #     value = value + '; False'

        if survey_question_search.question_type == 'matrix':
            value = ''
            for survey_user_input_line_reg in survey_user_input_line_search:
                if value == '':
                    value = survey_user_input_line_reg.suggested_answer_id.value
                else:
                    if survey_user_input_line_reg.suggested_answer_id.value is not False:
                        value = value + '; ' + survey_user_input_line_reg.suggested_answer_id.value

        return value


class SurveyUserInput_2(models.Model):
    _inherit = 'survey.user_input'

    state_2 = fields.Selection(
        [('new', 'New'),
         ('returned', 'Returned'),
         ('checked', 'Checked'),
         ('validated', 'Validated'),
         ('discarded', 'Discarded'),
         ], string='State 2', default='new', readonly=True, required=True
    )

    @api.model
    def is_allowed_transition(self, old_state_2, new_state_2):
        return True

    def change_state_2(self, new_state_2):
        for survey_user_input in self:
            if survey_user_input.is_allowed_transition(survey_user_input.state_2, new_state_2):
                survey_user_input.state_2 = new_state_2
            else:
                raise UserError(
                    'Status transition (' + survey_user_input.state_2 + ', ' + new_state_2 + ') is not allowed!')

    def action_new(self):
        for survey_user_input in self:
            survey_user_input.change_state_2('new')

    def action_returned(self):
        for survey_user_input in self:
            survey_user_input.change_state_2('returned')

    def action_checked(self):
        for survey_user_input in self:
            survey_user_input.change_state_2('checked')

    def action_validated(self):
        for survey_user_input in self:
            survey_user_input.change_state_2('validated')

    def action_discarded(self):
        for survey_user_input in self:
            survey_user_input.change_state_2('discarded')


class SurveyUserInput_3(models.Model):
    _inherit = 'survey.user_input'

    notes = fields.Text(string='Notes')

    parameter_1 = fields.Char(string='Parameter 1', required=False)
    parameter_2 = fields.Char(string='Parameter 2', required=False)
    parameter_3 = fields.Char(string='Parameter 3', required=False)
    parameter_4 = fields.Char(string='Parameter 4', required=False)


class SurveyUserInput_4(models.Model):
    _inherit = 'survey.user_input'

    def _survey_user_input_refresh(self):
        # self.ensure_one()

        for survey_user_input in self:

            referenceable_models = self.env['clv.referenceable.model'].search([
                ('base_model', '=', survey_user_input._name)])

            _logger.info(u'%s %s %s %s', '>>>>>',
                         survey_user_input._name, survey_user_input.access_token,
                         survey_user_input.ref_id)

            if survey_user_input.state_2 in ['new', 'returned', 'checked']:

                survey_user_input.state_2 = 'checked'
                survey_user_input.notes = False

                survey_user_input.ref_id = False
                survey_user_input.parameter_1 = False
                survey_user_input.parameter_2 = False
                survey_user_input.parameter_3 = False
                survey_user_input.parameter_4 = False

                parameter_1 = False
                parameter_2 = False
                parameter_3 = False
                parameter_4 = False

                for user_input_line in survey_user_input.user_input_line_ids:

                    question_parameter = user_input_line.question_id.parameter
                    value_char_box = user_input_line.value_char_box

                    if question_parameter == 'parameter_1':
                        parameter_1 = format_code(value_char_box)
                        survey_user_input.parameter_1 = parameter_1

                    if question_parameter == 'parameter_2':
                        parameter_2 = format_code(value_char_box)
                        survey_user_input.parameter_2 = parameter_2

                    if question_parameter == 'parameter_3':
                        parameter_3 = format_code(value_char_box)
                        survey_user_input.parameter_3 = parameter_3

                    if question_parameter == 'parameter_4':
                        parameter_4 = format_code(value_char_box)
                        survey_user_input.parameter_4 = parameter_4

                if survey_user_input.state in ['new', 'in_progress']:

                    survey_user_input.state_2 = 'returned'
                    if survey_user_input.notes is False:
                        survey_user_input.notes = \
                            u'Erro: A Entrada de Respostas ainda não foi concluída!'
                    else:
                        survey_user_input.notes += \
                            u'\nErro: A Entrada de Respostas ainda não foi concluída!'

                if parameter_1 is not False:

                    found_referenceable_model = False

                    for referenceable_model in referenceable_models:

                        Model = self.env[referenceable_model.model]

                        model = Model.search([
                            ('code', '=', survey_user_input.parameter_1),
                        ])

                        if model.id is not False:

                            if model.survey_id != survey_user_input.survey_id:

                                survey_user_input.state_2 = 'returned'
                                if survey_user_input.notes is False:
                                    survey_user_input.notes = u'Erro: Tipo de Pesquisa inválido!'
                                else:
                                    survey_user_input.notes += u'\nErro: Tipo de Pesquisa inválido!'

                            else:

                                survey_user_input.ref_id = model._name + ',' + str(model.id)

                                if parameter_2 is not False:

                                    if model.ref_id.code != parameter_2:

                                        survey_user_input.state_2 = 'returned'
                                        if survey_user_input.notes is False:
                                            survey_user_input.notes = u'Erro: Código "Refers to (Code)" inválido!'
                                        else:
                                            survey_user_input.notes += u'\nErro: Código "Refers to (Code)" inválido!'

                            found_referenceable_model = True

                    if found_referenceable_model is False:

                        survey_user_input.state_2 = 'returned'
                        if survey_user_input.notes is False:
                            survey_user_input.notes = u'Erro: Código "Refers to (Code)" inválido!'
                        else:
                            survey_user_input.notes += u'\nErro: Código "Refers to (Code)" inválido!'

                else:

                    if survey_user_input.state_2 in ['new', 'returned', 'checked']:

                        survey_user_input.state_2 = 'new'
                        survey_user_input.notes = False

                        survey_user_input.ref_id = False
                        survey_user_input.parameter_1 = False
                        survey_user_input.parameter_2 = False
                        survey_user_input.parameter_3 = False
                        survey_user_input.parameter_4 = False

        return True

    def _survey_user_input_validate(self):
        # self.ensure_one()

        for survey_user_input in self:

            _logger.info(u'%s %s %s', '>>>>>',
                         survey_user_input._name, survey_user_input.access_token)

            if survey_user_input.state in ['new', 'in_progress']:

                survey_user_input.state_2 = 'returned'
                if survey_user_input.notes is False:
                    survey_user_input.notes = \
                        u'Erro: A Entrada de Respostas ainda não foi concluída!'
                else:
                    survey_user_input.notes += \
                        u'\nErro: A Entrada de Respostas ainda não foi concluída!'

            elif survey_user_input.state_2 in ['checked', 'validated']:

                if survey_user_input.ref_id.survey_user_input_id.id is not False:

                    if survey_user_input.ref_id.survey_user_input_id.id != survey_user_input.id:

                        survey_user_input.state_2 = 'returned'
                        if survey_user_input.notes is False:
                            survey_user_input.notes = \
                                u'Erro: A Referência já está associada a outra Entrada de Respostas!'
                        else:
                            survey_user_input.notes += \
                                u'\nErro: A Referência já está associada a outra Entrada de Respostas!'

                    else:

                        survey_user_input.state_2 = 'validated'
                        survey_user_input.ref_id.reg_state = 'revised'
                        # survey_user_input.ref_id.state = 'waiting'
                        survey_user_input.ref_id.state = 'available'
                        survey_user_input.ref_id.items_ok = False

                else:

                    survey_user_input.ref_id.survey_user_input_id = survey_user_input.id
                    survey_user_input.ref_id.reg_state = 'revised'
                    survey_user_input.state_2 = 'validated'
                    # survey_user_input.ref_id.state = 'waiting'
                    survey_user_input.ref_id.state = 'available'
                    survey_user_input.ref_id.items_ok = False

        return True

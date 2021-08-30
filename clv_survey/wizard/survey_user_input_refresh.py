# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import re

from odoo import fields, models

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


class SurveyUserInputRefresh(models.TransientModel):
    _description = 'Survey User Input Refresh'
    _name = 'survey.user_input.refresh'

    def _default_survey_user_input_ids(self):
        return self._context.get('active_ids')
    survey_user_input_ids = fields.Many2many(
        comodel_name='survey.user_input',
        relation='survey_user_input_refresh_rel',
        string='Survey User Inputs',
        default=_default_survey_user_input_ids
    )

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

    def do_survey_user_input_refresh(self):
        self.ensure_one()

        for survey_user_input in self.survey_user_input_ids:

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
                            survey_user_input.notes = u'Erro: Código do Documento inválido!'
                        else:
                            survey_user_input.notes += u'\nErro: Código do Documento inválido!'

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

    def do_populate_all_survey_user_inputs(self):
        self.ensure_one()

        SurveyUserInput = self.env['survey.user_input']
        survey_user_inputs = SurveyUserInput.search([])

        self.survey_user_input_ids = survey_user_inputs

        return self._reopen_form()

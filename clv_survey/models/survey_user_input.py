# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from werkzeug import urls

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


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
        SurveyLabel = self.env['survey.label']
        SurveyUserInput = self.env['survey.user_input_line']

        survey_question_search = SurveyQuestion.search([
            ('code', '=', question_code[:11]),
        ])
        if question_code[:11] == question_code:
            survey_user_input_line_search = SurveyUserInput.search([
                ('user_input_id', '=', self.id),
                ('question_id', '=', survey_question_search.id),
            ])
        else:
            survey_label_search = SurveyLabel.search([
                ('code', '=', question_code),
            ])
            survey_user_input_line_search = SurveyUserInput.search([
                ('user_input_id', '=', self.id),
                ('question_id', '=', survey_question_search.id),
                ('value_suggested_row', '=', survey_label_search.id),
            ])

        value = False

        if survey_question_search.question_type == 'textbox':
            value = survey_user_input_line_search.value_text

        if survey_question_search.question_type == 'simple_choice':
            value = ''
            if question_code[11:13] == '_C':
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if survey_user_input_line_reg.value_text is not False:
                        value = survey_user_input_line_reg.value_text
            else:
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if value == '':
                        value = survey_user_input_line_reg.value_suggested.value
                    else:
                        if survey_user_input_line_reg.value_suggested.value is not False:
                            value = value + '; ' + survey_user_input_line_reg.value_suggested.value
                        # else:
                        #     value = value + '; False'
                # value = survey_user_input_line_search.value_suggested.value

        if survey_question_search.question_type == 'multiple_choice':
            value = ''
            if question_code[11:13] == '_C':
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if survey_user_input_line_reg.value_text is not False:
                        value = survey_user_input_line_reg.value_text
            else:
                for survey_user_input_line_reg in survey_user_input_line_search:
                    if value == '':
                        value = survey_user_input_line_reg.value_suggested.value
                    else:
                        if survey_user_input_line_reg.value_suggested.value is not False:
                            value = value + '; ' + survey_user_input_line_reg.value_suggested.value
                        # else:
                        #     value = value + '; False'

        if survey_question_search.question_type == 'matrix':
            value = ''
            for survey_user_input_line_reg in survey_user_input_line_search:
                if value == '':
                    value = survey_user_input_line_reg.value_suggested.value
                else:
                    if survey_user_input_line_reg.value_suggested.value is not False:
                        value = value + '; ' + survey_user_input_line_reg.value_suggested.value

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

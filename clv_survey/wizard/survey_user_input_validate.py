# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInputValidate(models.TransientModel):
    _description = 'Survey User Input Validate'
    _name = 'survey.user_input.validate'

    def _default_survey_user_input_ids(self):
        return self._context.get('active_ids')
    survey_user_input_ids = fields.Many2many(
        comodel_name='survey.user_input',
        relation='survey_user_input_validate_rel',
        string='Survey User Inputs',
        default=_default_survey_user_input_ids
    )

    survey_user_input_reflesh_exec = fields.Boolean(
        string='Survey User Input Refresh Execute',
        default=True
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

    def do_survey_user_input_validate(self):
        self.ensure_one()

        for survey_user_input in self.survey_user_input_ids:

            if self.survey_user_input_reflesh_exec:
                survey_user_input._survey_user_input_refresh()

            survey_user_input._survey_user_input_validate()

        return True

    def do_populate_all_survey_user_inputs(self):
        self.ensure_one()

        SurveyUserInput = self.env['survey.user_input']
        survey_user_inputs = SurveyUserInput.search([])

        self.survey_user_input_ids = survey_user_inputs

        return self._reopen_form()

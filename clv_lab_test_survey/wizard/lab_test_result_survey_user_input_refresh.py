# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultSurveyUserInputRefresh(models.TransientModel):
    _description = 'Survey User Input Refresh'
    _name = 'clv.lab_test.result.survey_user_input_refresh'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_survey_user_input_refresh_rel',
        string='Lab Test Results',
        default=_default_lab_test_result_ids
    )

    def do_lab_test_result_survey_user_input_refresh(self):
        self.ensure_one()

        for lab_test_result in self.lab_test_result_ids:

            lab_test_result.survey_user_input_id._survey_user_input_refresh()

        return True

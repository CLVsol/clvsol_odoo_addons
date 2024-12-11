# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultSurveyUserInputSetInProgress(models.TransientModel):
    _description = 'Survey User Input Set In Progress'
    _name = 'clv.lab_test.result.survey_user_input_set_in_progress'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_survey_user_input_set_in_progress_rel',
        string='Lab Test Results',
        default=_default_lab_test_result_ids
    )

    def do_lab_test_result_survey_user_input_set_in_progress(self):
        self.ensure_one()

        for lab_test_result in self.lab_test_result_ids:

            if lab_test_result.survey_user_input_id.id is not False:

                lab_test_result.survey_user_input_id.state = 'in_progress'
                lab_test_result.survey_user_input_id.state_2 = 'returned'

                lab_test_result.reg_state = 'revised'
                lab_test_result.state = 'available'

        return True

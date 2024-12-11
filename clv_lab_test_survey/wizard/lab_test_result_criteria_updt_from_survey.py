# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultCriteriaUpdateFromSurvey(models.TransientModel):
    _description = 'Lab Test Result Criteria Update from Survey'
    _name = 'clv.lab_test.result.criteria_updt_from_survey'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_criteria_updt_from_survey_rel',
        string='Lab Test Results',
        default=_default_lab_test_result_ids
    )

    def do_lab_test_result_criteria_updt_from_survey(self):
        self.ensure_one()

        for lab_test_result in self.lab_test_result_ids:

            _logger.info(u'%s %s %s', '>>>>>', lab_test_result.code, lab_test_result.lab_test_type_id.name)

            if lab_test_result.survey_user_input_id.id is not False:

                for criterion in lab_test_result.criterion_ids:

                    _logger.info(u'%s %s', '>>>>>>>>>>', criterion.code)

                    if criterion.code is not False:

                        criterion.result = lab_test_result.survey_user_input_id.get_value(criterion.code)

        return True

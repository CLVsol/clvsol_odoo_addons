# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultCriteriaRefresh(models.TransientModel):
    _description = 'Lab Test Result  Criteria Refresh'
    _name = 'clv.lab_test.result.criteria_refresh'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_criteria_refresh_rel',
        string='Lab Test Results',
        default=_default_lab_test_result_ids
    )

    def do_lab_test_result_criteria_refresh(self):
        self.ensure_one()

        LabTestCriteria = self.env['clv.lab_test.criterion']

        for lab_test_result in self.lab_test_result_ids:

            _logger.info(u'%s %s %s', '>>>>>', lab_test_result.code, lab_test_result.lab_test_type_id.name)

            criteria = []
            for criterion in lab_test_result.lab_test_type_id.criterion_ids:

                lab_test_result_criterion = LabTestCriteria.search([
                    ('lab_test_result_id', '=', lab_test_result.id),
                    ('code', '=', criterion.code),
                ])

                if lab_test_result_criterion.id is not False:
                    lab_test_result_criterion.sequence = criterion.sequence
                else:
                    if criterion.result_display:
                        criteria.append((0, 0, {'code': criterion.code,
                                                'name': criterion.name,
                                                'sequence': criterion.sequence,
                                                'unit_id': criterion.unit_id.id,
                                                'result': criterion.result,
                                                'normal_range': criterion.normal_range,
                                                # 'lab_test_type_id': criterion.lab_test_type_id.id,
                                                'sequence': criterion.sequence,
                                                'result_display': criterion.result_display,
                                                'report_display': criterion.report_display,
                                                }))

            lab_test_result.criterion_ids = criteria

            _logger.info(u'%s %s', '>>>>>>>>>>', criteria)

        return True

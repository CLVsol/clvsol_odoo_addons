# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class LabTestReportGetResults(models.TransientModel):
    _name = 'clv.lab_test.report.get_results'

    def _default_lab_test_report_ids(self):
        return self._context.get('active_ids')
    lab_test_report_ids = fields.Many2many(
        comodel_name='clv.lab_test.report',
        relation='clv_lab_test_report_lab_test_report_get_results_rel',
        string='Lab Test Requests',
        default=_default_lab_test_report_ids
    )

    @api.multi
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

    @api.multi
    def do_lab_test_report_get_results(self):
        self.ensure_one()

        for lab_test_report in self.lab_test_report_ids:

            _logger.info(u'%s %s %s', '>>>>>', lab_test_report.code, lab_test_report.person_id.name)
            _logger.info(u'%s %s %s', '>>>>>>>>>>',
                         lab_test_report.lab_test_request_id.code, lab_test_report.lab_test_request_id.person_id.name)

            for lab_test_result in lab_test_report.lab_test_request_id.lab_test_result_ids:

                _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>>', lab_test_result.code, lab_test_result.person_id.name)

                lab_test_result.lab_test_report_id = lab_test_report.id

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultReceive(models.TransientModel):
    _description = 'Lab Test Result Receive'
    _name = 'clv.lab_test.result.receive'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_lab_test_result_receive_rel',
        string='Lab Test Results',
        readonly=True,
        default=_default_lab_test_result_ids
    )

    def _default_employee_id(self):
        HrEmployee = self.env['hr.employee']
        employee = HrEmployee.search([
            ('user_id', '=', self.env.uid),
        ])
        if employee.id is not False:
            return employee.id
        return False
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Received by',
        required=True,
        default=_default_employee_id
    )

    date_received = fields.Datetime(
        string='Received Date',
        required=True,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    def do_lab_test_result_receive(self):
        self.ensure_one()

        current_phase_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip())

        for lab_test_result in self.lab_test_result_ids:

            _logger.info(u'%s %s %s', '>>>>>', lab_test_result.phase_id.id, lab_test_result.ref_name)

            if (lab_test_result.phase_id.id == current_phase_id) and \
               (lab_test_result.state == 'new'):

                _logger.info(u'%s %s %s', '>>>>>', self.employee_id.name, self.date_received)

                lab_test_result.employee_id_request = self.employee_id
                lab_test_result.date_received = self.date_received
                lab_test_result.state = 'received'
                lab_test_result.reg_state = 'revised'

        return True

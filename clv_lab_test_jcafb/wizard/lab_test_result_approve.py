# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class LabTestResultApprove(models.TransientModel):
    _description = 'Lab Test Result Approve'
    _name = 'clv.lab_test.result.approve'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_lab_test_result_approve_rel',
        string='Lab Test Results',
        readonly=True,
        default=_default_lab_test_result_ids
    )

    approved = fields.Boolean(string='Approved', default=True)

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
        string='Approved by',
        default=_default_employee_id
    )

    date_approved = fields.Date(
        string='Approved Date',
        default=lambda *a: datetime.now().strftime('%Y-%m-%d'),
    )

    def do_lab_test_result_approve(self):
        self.ensure_one()

        for lab_test_result in self.lab_test_result_ids:

            _logger.info(u'%s %s %s', '>>>>>', lab_test_result.code, lab_test_result.ref_id.name)

            _logger.info(u'%s %s %s', '>>>>>', self.employee_id.name, self.date_approved)

            if self.approved:

                lab_test_result.approved = self.approved
                lab_test_result.employee_id = self.employee_id
                lab_test_result.date_approved = self.date_approved
                lab_test_result.reg_state = 'done'
                lab_test_result.state = 'approved'

            else:

                lab_test_result.approved = False
                lab_test_result.employee_id = False
                lab_test_result.date_approved = False
                lab_test_result.reg_state = 'revised'
                lab_test_result.state = 'available'

        return True

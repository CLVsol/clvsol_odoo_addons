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
from odoo import exceptions

_logger = logging.getLogger(__name__)


class EmployeeDepartmentHistoryUpdate(models.TransientModel):
    _name = 'hr.employee.department_history_updt'

    def _default_employee_ids(self):
        return self._context.get('active_ids')
    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        relation='hr_employee_department_history_updt_rel',
        string='Employees',
        default=_default_employee_ids
    )
    new_department_sign_in_date = fields.Date(
        string='New department - Sign in date',
        required=False,
    )
    old_department_sign_out_date = fields.Date(
        string="Old department - Sign out date",
        required=False
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
    def do_employee_department_history_updt(self):
        self.ensure_one()

        HrEmployeeDepartmentHistory = self.env['hr.employee.department.history']

        for employee in self.employee_ids:

            if self.old_department_sign_out_date is False:
                raise exceptions.ValidationError('The "Old department - Sign out date" has not been defined!')
                return self._reopen_form()

            if self.new_department_sign_in_date is False:
                raise exceptions.ValidationError('The "New department - Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s %s', '>>>>>', employee.name, employee.department_id)

            if employee.department_id.id is not False:

                employee_department_history = HrEmployeeDepartmentHistory.search([
                    ('employee_id', '=', employee.id),
                    ('department_id', '=', employee.department_id.id),
                    ('sign_out_date', '=', False),
                ])

                if employee_department_history.id is False:

                    employee_department_history_2 = HrEmployeeDepartmentHistory.search([
                        ('employee_id', '=', employee.id),
                        ('sign_out_date', '=', False),
                    ])
                    if employee_department_history_2.id is not False:
                        employee_department_history_2.sign_out_date = self.old_department_sign_out_date
                        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', employee_department_history_2.department_id.name,
                                                     employee_department_history_2.sign_in_date,
                                                     employee_department_history_2.sign_out_date)

                    values = {
                        'employee_id': employee.id,
                        'department_id': employee.department_id.id,
                        'sign_in_date': self.new_department_sign_in_date,
                    }
                    employee_department_history = HrEmployeeDepartmentHistory.create(values)
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', employee_department_history.department_id.name,
                                                 employee_department_history.sign_in_date,
                                                 employee_department_history.sign_out_date)

                else:
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', employee_department_history.department_id.name,
                                                 employee_department_history.sign_in_date,
                                                 employee_department_history.sign_out_date)

            else:

                employee_department_history = HrEmployeeDepartmentHistory.search([
                    ('employee_id', '=', employee.id),
                    ('sign_out_date', '=', False),
                ])

                if employee_department_history.id is not False:
                    employee_department_history.sign_out_date = self.old_department_sign_out_date
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', employee_department_history.department_id.name,
                                                 employee_department_history.sign_in_date,
                                                 employee_department_history.sign_out_date)

        # return True
        return self._reopen_form()

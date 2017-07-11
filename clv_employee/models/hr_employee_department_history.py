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

from datetime import *

from odoo import fields, models


class EmployeeDepartmentHistory(models.Model):
    _description = 'Employee Department History'
    _name = 'hr.employee.department.history'
    _order = "sign_in_date desc"

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
        required=False
    )
    sign_in_date = fields.Date(
        string='Sign in date',
        required=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    sign_out_date = fields.Date(
        string="Sign out date",
        required=False
    )

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)


class Employee(models.Model):
    _inherit = 'hr.employee'

    employee_department_history_ids = fields.One2many(
        comodel_name='hr.employee.department.history',
        inverse_name='employee_id',
        string='Departments'
    )

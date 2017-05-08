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

from odoo import api, fields, models


class EmployeeLog(models.Model):
    _description = 'Employee Log'
    _name = 'hr.employee.log'
    _inherit = 'clv.object.log'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=True,
        ondelete='cascade'
    )


class Employee(models.Model):
    _name = "hr.employee"
    _inherit = 'hr.employee', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='hr.employee.log',
        inverse_name='employee_id',
        string='Employee Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, employee_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'employee_id': employee_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.env['hr.employee.log'].create(vals)

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


class EmployeeUserGroupsUpdt(models.TransientModel):
    _name = 'hr.employee.user_groups_updt'

    def _default_employee_ids(self):
        return self._context.get('active_ids')
    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        relation='hr_employee_user_groups_updt_rel',
        string='Employees',
        default=_default_employee_ids
    )
    count_employees = fields.Integer(
        string='Number of Employees',
        compute='_compute_count_employees',
        store=False
    )

    ref_employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Reference Employee'
    )

    group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='hr_employee_updt_group_rel',
        column1='employee_id',
        column2='group_id',
        string='Access Rights'
    )

    @api.depends('employee_ids')
    def _compute_count_employees(self):
        for r in self:
            r.count_employees = len(r.employee_ids)

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
    def do_employee_user_groups_updt(self):
        self.ensure_one()

        _logger.info(u'Employee User Groups Update on %s', self.employee_ids.ids)

        for employee_reg in self.employee_ids:

            _logger.info(u'%s %s', employee_reg.id, employee_reg.name)

            if employee_reg.user_id is not False:

                values = {
                    'groups_id': [(6, 0, [])],
                }
                employee_reg.user_id.write(values)

                for group in self.group_ids:
                    values = {
                        'groups_id': [(4, group.id)],
                    }
                    employee_reg.user_id.write(values)

        return True

    @api.multi
    def get_reference_Employee_access_rights(self):
        self.ensure_one()

        if self.ref_employee_id.user_id is not False:
            group_ids = []
            for group in self.ref_employee_id.user_id.groups_id:
                _logger.info(u'%s %s', group.id, group.name)
                group_ids.append(group.id)
            self.group_ids = group_ids

        return self._reopen_form()

    @api.multi
    def do_refresh_access_rights(self):
        self.ensure_one()

        return self._reopen_form()

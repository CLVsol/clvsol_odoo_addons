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


class EmployeeMngEmployeeCreate(models.TransientModel):
    _name = 'clv.employee.mng.employee_create'

    def _default_employee_mng_ids(self):
        return self._context.get('active_ids')
    employee_mng_ids = fields.Many2many(
        comodel_name='clv.employee.mng',
        relation='clv_employee_mng_employee_create_rel',
        string='Employees (Management)',
        default=_default_employee_mng_ids
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
    def do_employee_mng_employee_create(self):
        self.ensure_one()

        lang = 'pt_BR'  # use Translation: Portuguese(BR)/Portugues(BR)
        tz = 'America/Sao_Paulo'

        ResPartner = self.env['res.partner']
        ResUsers = self.env['res.users']
        HrEmployee = self.env['hr.employee']

        for employee_mng in self.employee_mng_ids:

            _logger.info(u'>>>>> %s', employee_mng.name)

            if employee_mng.partner_id is not False:
                partner = ResPartner.search([
                    ('name', '=', employee_mng.name),
                ])
                if partner.id is not False:

                    employee_mng.partner_id = partner.id

                    _logger.info(u'>>>>>>>>>> %s', employee_mng.partner_id.name)

                else:

                    values = {
                        'name': employee_mng.name,
                        'customer': False,
                        'employee': False,
                        'is_company': False,
                        'email': employee_mng.email,
                        'website': '',
                        'company_id': 1,
                        'tz': tz,
                        'lang': lang,
                    }
                    res_partner = ResPartner.create(values)
                    employee_mng.partner_id = res_partner.id

            if employee_mng.user_id is not False:
                user = ResUsers.search([
                    ('name', '=', employee_mng.name),
                    # ('login', '=', employee_mng.email),
                ])
                if user.id is not False:

                    employee_mng.user_id = user.id

                    _logger.info(u'>>>>>>>>>> %s', employee_mng.user_id.name)

                else:

                    password = employee_mng.email
                    password = password[:password.find('@')]

                    values = {
                        'name': employee_mng.name,
                        'partner_id': employee_mng.partner_id.id,
                        'company_id': 1,
                        'login': employee_mng.email,
                        'password': password,
                        'groups_id': [(6, 0, [])],
                    }
                    res_user = ResUsers.create(values)
                    employee_mng.user_id = res_user.id

            if employee_mng.employee_id is not False:
                employee = HrEmployee.search([
                    ('name', '=', employee_mng.name),
                ])
                if employee.id is not False:

                    employee_mng.employee_id = employee.id

                    employee.job_id = employee_mng.job_id.id
                    employee.department_id = employee_mng.department_id.id
                    employee.history_marker_id = employee_mng.history_marker_id.id

                    _logger.info(u'>>>>>>>>>> %s', employee_mng.employee_id.name)

                else:

                    values = {
                        'name': employee_mng.name,
                        'work_email': employee_mng.email,
                        'job_id': employee_mng.job_id.id,
                        'department_id': employee_mng.department_id.id,
                        'user_id': employee_mng.user_id.id,
                        'history_marker_id': employee_mng.history_marker_id.id,
                    }
                    employee = HrEmployee.create(values)
                    employee_mng.employee_id = employee.id

        return True

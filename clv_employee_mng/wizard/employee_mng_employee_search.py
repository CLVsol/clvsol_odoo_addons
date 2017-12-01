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


class HrEmployeeMngHrEmployeeSearch(models.TransientModel):
    _name = 'clv.employee.mng.employee_search'

    def _default_employee_mng_ids(self):
        return self._context.get('active_ids')
    employee_mng_ids = fields.Many2many(
        comodel_name='clv.employee.mng',
        relation='clv_employee_mng_employee_search_rel',
        string='HrEmployees (Management)',
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
    def do_employee_mng_employee_search(self):
        self.ensure_one()

        ResPartner = self.env['res.partner']
        ResUsers = self.env['res.users']
        HrEmployee = self.env['hr.employee']

        for employee_mng in self.employee_mng_ids:

            _logger.info(u'>>>>> %s', employee_mng.name)

            partner = ResPartner.search([
                ('name', '=', employee_mng.name),
            ])
            if partner.id is not False:

                employee_mng.partner_id = partner.id

                _logger.info(u'>>>>>>>>>> %s', employee_mng.partner_id.name)

            user = ResUsers.search([
                ('name', '=', employee_mng.name),
            ])
            if user.id is not False:

                employee_mng.user_id = user.id

                _logger.info(u'>>>>>>>>>> %s', employee_mng.user_id.name)

            employee = HrEmployee.search([
                ('name', '=', employee_mng.name),
            ])
            if employee.id is not False:

                employee_mng.employee_id = employee.id

                _logger.info(u'>>>>>>>>>> %s', employee_mng.employee_id.name)

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class EmployeeMassEdit(models.TransientModel):
    _inherit = 'hr.employee.mass_edit'

    token = fields.Char(
        string='Token', default=False,
        help='Use "/" to get an automatic new Token.'
    )
    token_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Token:', default=False, readonly=False, required=False
    )

    preset_user_password = fields.Boolean(
        string='Reset User Password'
    )

    def do_employee_mass_edit(self):
        self.ensure_one()

        super().do_employee_mass_edit()

        for employee in self.employee_ids:

            _logger.info(u'%s %s', '>>>>>', employee.name)

            if self.token_selection == 'set':
                employee.token = self.token
            if self.token_selection == 'remove':
                employee.token = False

            if self.preset_user_password:
                employee._preset_user_password()

        return True

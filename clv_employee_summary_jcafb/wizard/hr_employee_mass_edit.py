# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class EmployeeMassEdit(models.TransientModel):
    _inherit = 'hr.employee.mass_edit'

    summary_id = fields.Many2one(
        comodel_name='clv.summary',
        string='Summary'
    )
    summary_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Summary:', default=False, readonly=False, required=False
    )

    def do_employee_mass_edit(self):
        self.ensure_one()

        super().do_employee_mass_edit()

        for employee in self.employee_ids:

            _logger.info(u'%s %s', '>>>>>', employee.name)

            if self.summary_id_selection == 'set':
                employee.summary_id = self.summary_id
            if self.summary_id_selection == 'remove':
                employee.summary_id = False

            if self.phase_id_selection == 'set':
                employee.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                employee.phase_id = False

        return True

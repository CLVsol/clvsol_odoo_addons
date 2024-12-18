# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _name = "hr.employee"
    _inherit = 'hr.employee', 'clv.abstract.token'

    def _preset_user_password(self):

        for employee in self:

            _logger.info(u'%s %s', '>>>>> (employee):', employee.name)

            if employee.token is not False:
                employee.user_id.password = employee.token[:8]

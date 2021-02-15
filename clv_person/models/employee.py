# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Person(models.Model):
    _inherit = 'clv.person'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible Empĺoyee',
        # related='ref_address_id.employee_id',
        # store=True
        required=False,
        readonly=False
    )

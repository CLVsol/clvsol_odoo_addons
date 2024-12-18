# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    template_file_name_result = fields.Char(
        string='Template File Name (Result)',
        required=False,
        help="Template File Name (Result)"
    )

    template_file_name_report = fields.Char(
        string='Template File Name (Report)',
        required=False,
        help="Template File Name (Report)"
    )

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestRequest(models.Model):
    _description = 'Lab Test Request'
    _name = 'clv.lab_test.request'


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    lab_test_request_ids = fields.Integer(
        string='Lab Test Requests',
        default=False,
        readonly=True
    )

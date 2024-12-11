# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey Type')

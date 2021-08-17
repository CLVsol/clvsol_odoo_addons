# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SurveyUserInput(models.Model):
    _name = "survey.user_input"
    _inherit = 'survey.user_input', 'clv.abstract.reference'

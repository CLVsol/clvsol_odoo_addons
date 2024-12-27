# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GlobalLogClient(models.Model):
    _description = 'Global Log Client'
    _name = 'clv.global_log.client'
    _order = 'model_name'

    model_name = fields.Char(string='Model Name', required=True)
    notes = fields.Text(string='Notes')

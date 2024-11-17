# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class GlobalTag(models.Model):
    _description = 'Global Tag'
    _name = 'clv.global_tag'
    _inherit = 'clv.abstract.tag'

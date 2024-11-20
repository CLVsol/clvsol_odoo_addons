# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Patient(models.Model):
    _name = "clv.patient"
    _inherit = 'clv.patient', 'clv.abstract.random'

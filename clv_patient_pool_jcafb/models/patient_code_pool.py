# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PatientCodePool(models.Model):
    _description = 'Patient Code Pool'
    _name = "clv.patient.code_pool"
    _inherit = 'clv.abstract.pool'

    code_sequence = fields.Char(string='Code Sequence', default='clv.person.code')

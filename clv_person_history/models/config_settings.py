# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ConfigSettings(models.TransientModel):
    _inherit = 'clv.config.settings'

    default_phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Default Phase',
        ondelete='restrict',
        default_model='clv.person'
    )

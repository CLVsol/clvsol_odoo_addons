# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

PARAMS = [
    ("current_residence_name_format", "clv.global_settings.current_residence_name_format"),
]


class GlobalSettings(models.TransientModel):
    _inherit = 'clv.global_settings'

    current_residence_name_format = fields.Char(
        string='Residence Name Format',
        compute='_compute_current_residence_name_format',
        store=False,
    )

    def set_values(self):
        self.ensure_one()

        super().set_values()

        for field_name, key_name in PARAMS:
            value = str(getattr(self, field_name, '')).strip()
            self.env['ir.config_parameter'].set_param(key_name, value)

    def get_values(self):

        res = super().get_values()

        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '').strip()
        return res


class GlobalSettings_2(models.TransientModel):
    _inherit = 'clv.global_settings'

    residence_name_format = fields.Char(
        string='Residence Name Format:'
    )

    @api.depends('residence_name_format')
    def _compute_current_residence_name_format(self):
        for r in self:
            r.current_residence_name_format = r.residence_name_format

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        current_residence_name_format = defaults['current_residence_name_format']
        defaults['residence_name_format'] = current_residence_name_format

        return defaults

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

PARAMS = [
    ("current_history_marker_id", "clv.config.settings.current_history_marker_id"),
]


class ConfigSettings(models.TransientModel):
    _inherit = 'clv.config.settings'

    current_history_marker_id = fields.Char(
        string='Current History Marker',
        compute='_compute_current_history_marker_id',
        store=False,
    )

    @api.multi
    def set_params(self):
        self.ensure_one()

        for field_name, key_name in PARAMS:
            value = str(getattr(self, field_name, '')).strip()
            self.env['ir.config_parameter'].set_param(key_name, value)

    def get_default_params(self, fields):
        res = {}
        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '').strip()
        return res


class ConfigSettings_2(models.TransientModel):
    _inherit = 'clv.config.settings'

    history_marker_id = fields.Many2one(
        comodel_name='clv.history_marker',
        string='Current History Marker',
        ondelete='restrict',
    )

    @api.depends('history_marker_id')
    def _compute_current_history_marker_id(self):
        for r in self:
            r.current_history_marker_id = r.history_marker_id.id

    @api.model
    def default_get(self, field_names):

        defaults = super(ConfigSettings_2, self).default_get(field_names)

        HistoryMarker = self.env['clv.history_marker']
        current_history_marker_id = False
        if defaults['current_history_marker_id'] != '' and \
           defaults['current_history_marker_id'] != 'False':
            current_history_marker_id = defaults['current_history_marker_id']
        history_marker = HistoryMarker.search([
            ('id', '=', current_history_marker_id),
        ])
        defaults['history_marker_id'] = history_marker.id

        return defaults

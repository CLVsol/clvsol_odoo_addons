# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

PARAMS = [
    ("current_date_reference", "clv.global_settings.current_date_reference"),
    # ("current_phase_id", "clv.global_settings.current_phase_id"),
]


class GlobalSettings(models.TransientModel):
    _inherit = 'clv.global_settings'

    current_date_reference = fields.Date(
        string='Current Reference Date',
        compute='_compute_current_date_reference',
        store=False,
    )

    # current_phase_id = fields.Char(
    #     string='Current Phase',
    #     compute='_compute_current_phase_id',
    #     store=False,
    # )

    @api.multi
    def set_values(self):
        self.ensure_one()

        super(GlobalSettings, self).set_values()

        for field_name, key_name in PARAMS:
            value = str(getattr(self, field_name, '')).strip()
            self.env['ir.config_parameter'].set_param(key_name, value)

    def get_values(self):

        res = super(GlobalSettings, self).get_values()

        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '').strip()
        return res


class GlobalSettings_2(models.TransientModel):
    _inherit = 'clv.global_settings'

    date_reference = fields.Date(string="Current Reference Date:")

    # phase_id = fields.Many2one(
    #     comodel_name='clv.phase',
    #     string='Current Phase:',
    #     ondelete='restrict',
    # )

    @api.depends('date_reference')
    def _compute_current_date_reference(self):
        for r in self:
            r.current_date_reference = r.date_reference

    # @api.depends('phase_id')
    # def _compute_current_phase_id(self):
    #     for r in self:
    #         r.current_phase_id = r.phase_id.id

    @api.model
    def default_get(self, field_names):

        defaults = super(GlobalSettings_2, self).default_get(field_names)

        current_date_reference = defaults['current_date_reference']
        defaults['date_reference'] = current_date_reference

        # Phase = self.env['clv.phase']

        # current_phase_id = False
        # try:
        #     if defaults['current_phase_id'] != '' and \
        #        defaults['current_phase_id'] != 'False':
        #         current_phase_id = defaults['current_phase_id']
        # except KeyError:
        #     pass

        # phase = Phase.search([
        #     ('id', '=', current_phase_id),
        # ])
        # defaults['phase_id'] = phase.id

        return defaults

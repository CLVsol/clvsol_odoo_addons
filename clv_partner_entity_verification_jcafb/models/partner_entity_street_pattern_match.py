# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerEntityStreetPatternMatch(models.Model):
    _description = 'Partner Entity Street Pattern Match'
    _name = 'clv.partner_entity.street_pattern.match'

    street_pattern_id = fields.Many2one(
        comodel_name='clv.partner_entity.street_pattern',
        string='Partner Entity Street Pattern',
        required=False
    )

    notes = fields.Text(string='Notes')


class PartnerEntityStreetPattern(models.Model):
    _inherit = 'clv.partner_entity.street_pattern'

    street_pattern_match_ids = fields.One2many(
        comodel_name='clv.partner_entity.street_pattern.match',
        inverse_name='street_pattern_id',
        string='Street Pattern Matches',
        readonly=True
    )
    count_street_pattern_matches = fields.Integer(
        string='Number of Matches',
        compute='_compute_count_street_pattern_matches',
        store=True,
    )

    @api.depends('street_pattern_match_ids')
    def _compute_count_street_pattern_matches(self):
        for r in self:
            r.count_street_pattern_matches = len(r.street_pattern_match_ids)

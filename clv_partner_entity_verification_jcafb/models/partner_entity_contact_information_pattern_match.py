# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerEntityContactInformationPatternMatch(models.Model):
    _description = 'Partner Entity Contact_Information Pattern Match'
    _name = 'clv.partner_entity.contact_information_pattern.match'

    contact_information_pattern_id = fields.Many2one(
        comodel_name='clv.partner_entity.contact_information_pattern',
        string='Partner Entity Contact_Information Pattern',
        required=False
    )

    notes = fields.Text(string='Notes')


class PartnerEntityContactInformationPattern(models.Model):
    _inherit = 'clv.partner_entity.contact_information_pattern'

    contact_information_pattern_match_ids = fields.One2many(
        comodel_name='clv.partner_entity.contact_information_pattern.match',
        inverse_name='contact_information_pattern_id',
        string='Contact_Information Pattern Matches',
        readonly=True
    )
    count_contact_information_pattern_matches = fields.Integer(
        string='Number of Matches',
        compute='_compute_count_contact_information_pattern_matches',
        store=True,
    )

    @api.depends('contact_information_pattern_match_ids')
    def _compute_count_contact_information_pattern_matches(self):
        for r in self:
            r.count_contact_information_pattern_matches = len(r.contact_information_pattern_match_ids)

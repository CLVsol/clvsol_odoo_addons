# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PartnerEntityStreetPatternMatch(models.Model):
    _name = "clv.partner_entity.street_pattern.match"
    _inherit = 'clv.partner_entity.street_pattern.match', 'clv.abstract.reference'


class PartnerEntityContactInformationPatternMatch(models.Model):
    _name = "clv.partner_entity.contact_information_pattern.match"
    _inherit = 'clv.partner_entity.contact_information_pattern.match', 'clv.abstract.reference'

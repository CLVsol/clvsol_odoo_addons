# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PartnerStreetPatterntSearch(models.TransientModel):
    _description = 'Partner Street Pattern Search'
    _name = 'res.partner.street_pattern.search'

    def _default_res_partner_ids(self):
        return self._context.get('active_ids')
    res_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='res_partner_street_pattern_search_rel',
        string='Partners',
        readonly=True,
        default=_default_res_partner_ids
    )

    street_pattern_id = fields.Many2one(
        comodel_name='clv.partner_entity.street_pattern',
        string='Partner Entity Street Pattern',
    )

    def do_res_partner_street_pattern_search(self):
        self.ensure_one()

        for res_partner in self.res_partner_ids:

            _logger.info(u'%s %s %s', '>>>>>', self.street_pattern_id.street_name, self.street_pattern_id.district)

            res_partner.street_name = self.street_pattern_id.street_name
            res_partner.district = self.street_pattern_id.district

        return True

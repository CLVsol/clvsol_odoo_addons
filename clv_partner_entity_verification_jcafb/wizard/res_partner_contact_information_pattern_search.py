# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
# from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PartnerContactInformaationPatterntSearch(models.TransientModel):
    _description = 'Partner Contact Informaation Pattern Search'
    _name = 'res.partner.contact_information_pattern.search'

    def _default_res_partner_ids(self):
        return self._context.get('active_ids')
    res_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='res_partner_contact_information_pattern_search_rel',
        string='Partners',
        readonly=True,
        default=_default_res_partner_ids
    )

    contact_information_pattern_id = fields.Many2one(
        comodel_name='clv.partner_entity.contact_information_pattern',
        string='Partner Entity Contact_Information Pattern',
    )

    def do_res_partner_contact_information_pattern_search(self):
        self.ensure_one()

        for res_partner in self.res_partner_ids:

            _logger.info(u'%s %s %s %s %s', '>>>>>',
                         self.contact_information_pattern_id.street_name,
                         self.contact_information_pattern_id.street_number,
                         self.contact_information_pattern_id.street2,
                         self.contact_information_pattern_id.district
                         )

            res_partner.street_name = self.contact_information_pattern_id.street_name
            res_partner.street_number = self.contact_information_pattern_id.street_number
            res_partner.street2 = self.contact_information_pattern_id.street2
            res_partner.district = self.contact_information_pattern_id.district

        return True

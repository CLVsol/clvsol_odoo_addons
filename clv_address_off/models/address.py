# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AddressOff(models.Model):
    _inherit = 'clv.address_off'

    related_address_id = fields.Many2one(comodel_name='clv.address', string='Related Address', ondelete='restrict')
    related_address_name = fields.Char(string='Related Address Name', related='related_address_id.name')
    related_address_code = fields.Char(string='Related Address Code', related='related_address_id.code')
    related_address_category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        string='Related Address Categories',
        related='related_address_id.category_ids'
    )

    @api.multi
    def do_address_off_get_related_address_data(self):

        for address_off in self:

            _logger.info(u'>>>>> %s', address_off.related_address_id)

            if (address_off.reg_state in ['draft', 'revised']) and \
               (address_off.related_address_id.id is not False):

                data_values = {}
                # data_values['name'] = address_off.related_address_id.name
                data_values['code'] = address_off.related_address_id.code

                data_values['street'] = address_off.related_address_id.street
                data_values['street2'] = address_off.related_address_id.street2
                data_values['zip'] = address_off.related_address_id.zip
                data_values['city'] = address_off.related_address_id.city
                data_values['state_id'] = address_off.related_address_id.state_id.id
                data_values['country_id'] = address_off.related_address_id.country_id.id
                data_values['phone'] = address_off.related_address_id.phone
                data_values['mobile'] = address_off.related_address_id.mobile

                _logger.info(u'>>>>>>>>>> %s', data_values)

                address_off.write(data_values)

        return True

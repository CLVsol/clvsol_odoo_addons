# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Address(models.Model):
    _inherit = 'clv.address'

    is_residence = fields.Boolean(
        string='Is Residence',
        default=False
    )

    residence_ids = fields.One2many(
        comodel_name='clv.residence',
        inverse_name='ref_address_id',
        string='Residences'
    )
    count_residences = fields.Integer(
        string='Residences (count)',
        compute='_compute_count_residences',
        store=False
    )

    # @api.depends('residence_ids')
    def _compute_count_residences(self):
        for r in self:
            r.count_residences = len(r.residence_ids)


class Residence(models.Model):
    _inherit = 'clv.residence'

    ref_address_is_unavailable = fields.Boolean(
        string='Address is unavailable',
        default=False,
    )
    ref_address_id = fields.Many2one(comodel_name='clv.address', string='Address', ondelete='restrict')
    ref_address_code = fields.Char(string='Address Code', related='ref_address_id.code', store=False)

    ref_address_phone = fields.Char(string='Address Phone', related='ref_address_id.phone')
    ref_address_mobile_phone = fields.Char(string='Address Mobile', related='ref_address_id.mobile')
    ref_address_email = fields.Char(string='Address Email', related='ref_address_id.email')

    ref_address_category_names = fields.Char(
        string='Address Category Names',
        related='ref_address_id.category_ids.name',
        store=True
    )
    ref_address_category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        string='Address Categories',
        related='ref_address_id.category_ids'
    )

    def do_residence_get_ref_address_data(self):

        for residence in self:

            _logger.info(u'>>>>> %s', residence.ref_address_id)

            if (residence.ref_address_id.id is not False):

                data_values = {}

                if residence.ref_address_id.id is not False:

                    data_values['ref_address_id'] = residence.ref_address_id.id

                    data_values['street_name'] = residence.ref_address_id.street_name
                    data_values['street_number'] = residence.ref_address_id.street_number
                    data_values['street_number2'] = residence.ref_address_id.street_number2
                    data_values['street2'] = residence.ref_address_id.street2
                    data_values['zip'] = residence.ref_address_id.zip
                    data_values['city'] = residence.ref_address_id.city
                    data_values['city_id'] = residence.ref_address_id.city_id.id
                    data_values['state_id'] = residence.ref_address_id.state_id.id
                    data_values['country_id'] = residence.ref_address_id.country_id.id
                    if self.updt_phone:
                        data_values['phone'] = residence.ref_address_id.phone
                    if self.updt_mobile:
                        data_values['mobile'] = residence.ref_address_id.mobile
                    if self.updt_email:
                        data_values['email'] = residence.ref_address_id.email

                _logger.info(u'>>>>>>>>>> %s', data_values)

                residence.write(data_values)

        return True


class Residence_2(models.Model):
    _inherit = 'clv.residence'

    ref_address_state = fields.Selection(
        string='Address State',
        related='ref_address_id.state',
        store=False
    )

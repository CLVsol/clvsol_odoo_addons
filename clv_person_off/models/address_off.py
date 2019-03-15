# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AddressOff(models.Model):
    _inherit = 'clv.address_off'

    person_off_ids = fields.One2many(
        comodel_name='clv.person_off',
        inverse_name='ref_address_off_id',
        string='Persons (Off)'
    )
    count_person_offs = fields.Integer(
        string='Persons (Off) (count)',
        compute='_compute_count_person_offs',
        # store=True
    )

    @api.depends('person_off_ids')
    def _compute_count_person_offs(self):
        for r in self:
            r.count_person_offs = len(r.person_off_ids)


class PersonOff(models.Model):
    _inherit = 'clv.person_off'

    ref_address_off_id = fields.Many2one(comodel_name='clv.address_off', string='Address (Off)', ondelete='restrict')
    ref_address_off_code = fields.Char(string='Address (Off) Code', related='ref_address_off_id.code', store=False)

    ref_address_off_phone = fields.Char(string='Address (Off) Phone', related='ref_address_off_id.phone')
    ref_address_off_mobile_phone = fields.Char(string='Address (Off) Mobile', related='ref_address_off_id.mobile')
    ref_address_off_email = fields.Char(string='Address (Off) Email', related='ref_address_off_id.email')

    ref_address_off_category_names = fields.Char(
        string='Address (Off) Category Names',
        related='ref_address_off_id.category_ids.name',
        store=True
    )
    ref_address_off_category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        string='Address (Off) Categories',
        related='ref_address_off_id.category_ids'
    )

    @api.multi
    def do_person_off_get_ref_address_off_data(self):

        for person_off in self:

            _logger.info(u'>>>>> %s', person_off.ref_address_off_id)

            if (person_off.reg_state in ['draft', 'revised']) and \
               (person_off.ref_address_off_id.id is not False):

                data_values = {}

                if person_off.ref_address_off_id.id is not False:

                    data_values['ref_address_off_id'] = person_off.ref_address_off_id.id

                    data_values['street'] = person_off.ref_address_off_id.street
                    data_values['street2'] = person_off.ref_address_off_id.street2
                    data_values['zip'] = person_off.ref_address_off_id.zip
                    data_values['city'] = person_off.ref_address_off_id.city
                    data_values['state_id'] = person_off.ref_address_off_id.state_id.id
                    data_values['country_id'] = person_off.ref_address_off_id.country_id.id
                    # data_values['phone'] = person_off.ref_address_off_id.phone
                    # data_values['mobile'] = person_off.ref_address_off_id.mobile

                _logger.info(u'>>>>>>>>>> %s', data_values)

                person_off.write(data_values)

        return True

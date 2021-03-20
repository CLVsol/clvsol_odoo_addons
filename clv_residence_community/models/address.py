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
        inverse_name='related_address_id',
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

    related_address_is_unavailable = fields.Boolean(
        string='Related Address is unavailable',
        default=True,
    )
    related_address_id = fields.Many2one(comodel_name='clv.address', string='Related Address', ondelete='restrict')
    related_address_code = fields.Char(string='Related Address Code', related='related_address_id.code', store=False)

    related_address_category_names = fields.Char(
        string='Related Address Category Names',
        related='related_address_id.category_ids.name',
        store=True
    )
    related_address_category_ids = fields.Many2many(
        comodel_name='clv.address.category',
        string='Related Address Categories',
        related='related_address_id.category_ids'
    )

    def do_residence_get_related_address_data(self):

        for residence in self:

            _logger.info(u'>>>>> %s', residence.related_address_id)

            if (residence.reg_state in ['draft', 'revised']) and \
               (residence.related_address_id.id is not False):

                data_values = {}
                data_values['name'] = residence.related_address_id.name
                data_values['code'] = residence.related_address_id.code

                data_values['contact_info_is_unavailable'] = residence.related_address_id.contact_info_is_unavailable

                data_values['street_name'] = residence.related_address_id.street_name
                data_values['street_number'] = residence.related_address_id.street_number
                data_values['street_number2'] = residence.related_address_id.street_number2
                data_values['street2'] = residence.related_address_id.street2
                data_values['zip'] = residence.related_address_id.zip
                data_values['city'] = residence.related_address_id.city
                data_values['city_id'] = residence.related_address_id.city_id.id
                data_values['state_id'] = residence.related_address_id.state_id.id
                data_values['country_id'] = residence.related_address_id.country_id.id
                data_values['phone'] = residence.related_address_id.phone
                data_values['mobile'] = residence.related_address_id.mobile

                data_values['state'] = residence.related_address_id.state

                data_values['phase_id'] = residence.related_address_id.phase_id.id

                PatientCategory = self.env['clv.residence.category']
                m2m_list = []
                for address_category_id in residence.related_address_id.category_ids:
                    residence_category = PatientCategory.search([
                        ('name', '=', address_category_id.name),
                    ])
                    m2m_list.append((4, residence_category.id))
                data_values['category_ids'] = m2m_list

                data_values['employee_id'] = residence.related_address_id.employee_id.id

                PatientMarker = self.env['clv.residence.marker']
                m2m_list = []
                for address_marker_id in residence.related_address_id.marker_ids:
                    residence_marker = PatientMarker.search([
                        ('name', '=', address_marker_id.name),
                    ])
                    m2m_list.append((4, residence_marker.id))
                data_values['marker_ids'] = m2m_list

                _logger.info(u'>>>>>>>>>> %s', data_values)

                residence.write(data_values)

        return True


class Residence_2(models.Model):
    _inherit = 'clv.residence'

    related_address_state = fields.Selection(
        string='Address State',
        related='related_address_id.state',
        store=False
    )

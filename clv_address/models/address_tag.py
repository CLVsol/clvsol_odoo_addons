# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AddressTag(models.Model):
    _description = 'Address Tag'
    _name = 'clv.address.tag'
    _inherit = 'clv.abstract.tag'

    code = fields.Char(string='Tag Code', required=False)

    address_ids = fields.Many2many(
        comodel_name='clv.address',
        relation='clv_address_tag_rel',
        column1='tag_id',
        column2='address_id',
        string='Addresses'
    )


class Address(models.Model):
    _inherit = "clv.address"

    tag_ids = fields.Many2many(
        comodel_name='clv.address.tag',
        relation='clv_address_tag_rel',
        column1='address_id',
        column2='tag_id',
        string='Address Tags'
    )
    tag_names = fields.Char(
        string='Tag Names',
        compute='_compute_tag_names',
        store=True
    )

    @api.depends('tag_ids')
    def _compute_tag_names(self):
        for r in self:
            tag_names = False
            for tag in r.tag_ids:
                if tag_names is False:
                    tag_names = tag.name
                else:
                    tag_names = tag_names + ', ' + tag.name
            r.tag_names = tag_names

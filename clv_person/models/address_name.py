# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Person(models.Model):
    _inherit = 'clv.person'

    address_name = fields.Char(
        string="Address Name",
        required=False,
        store=True,
        compute="_get_address_name",
        help='Address Name for the Address.'
    )

    @api.depends('street_name', 'street_number', 'street_number2', 'street2')
    def _get_address_name(self):
        for record in self:
            if record.street_name:
                record.address_name = record.street_name
                if record.street_number:
                    record.address_name = record.address_name + ', ' + record.street_number
                    if record.street_number2:
                        record.address_name = record.address_name + '/' + record.street_number2
                else:
                    if record.street_number2:
                        record.address_name = record.address_name + ', ' + record.street_number2
                if record.street2:
                    record.address_name = record.address_name + ' (' + record.street2 + ')'
            else:
                record.address_name = 'Address Name...'

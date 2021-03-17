# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Residence(models.Model):
    _inherit = 'clv.residence'

    suggested_name = fields.Char(
        string="Suggested Name", required=False, store=True,
        compute="_get_suggested_name",
        help='Suggested Name for the Residence.'
    )
    automatic_set_name = fields.Boolean(
        string='Automatic Name',
        help="If checked, the Residence Name will be set automatically.",
        default=True
    )

    @api.depends('street_name', 'street_number', 'street_number2', 'street2')
    def _get_suggested_name(self):
        for record in self:
            if record.street_name:
                address_name = record.street_name
                if record.street_number:
                    address_name = address_name + ', ' + record.street_number
                    if record.street_number2:
                        address_name = address_name + '/' + record.street_number2
                else:
                    if record.street_number2:
                        address_name = address_name + ', ' + record.street_number2
                if record.street2:
                    address_name = address_name + ' (' + record.street2 + ')'
                residence_name_format = self.env['ir.config_parameter'].sudo().get_param(
                    'clv.global_settings.current_residence_name_format', '').strip()
                residence_name = residence_name_format.replace('<address_name>', address_name)
                record.suggested_name = residence_name
            else:
                record.suggested_name = 'Residence Name...'

    @api.model
    def create(self, values):
        record = super().create(values)

        if record.automatic_set_name:
            if record.name != record.suggested_name:
                record['name'] = record.suggested_name

        return record

    def write(self, values):
        ret = super().write(values)
        for record in self:
            if record.suggested_name is not False:
                if record.automatic_set_name:
                    if record.name != record.suggested_name:
                        values['name'] = record.suggested_name
                        super().write(values)
                else:
                    if ('name' in values and values['name'] == '/') or \
                       (record.name == '/'):
                        values['name'] = record.suggested_name
                        super().write(values)
        return ret

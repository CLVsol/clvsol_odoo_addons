# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.modules import get_module_resource


class Address(models.Model):

    _name = 'clv.address'
    _description = 'Address'
    _inherit = 'clv.abstract.partner_entity'

    code = fields.Char(string='Address Code', required=False)

    @api.model
    def _create_vals(self, vals):
        vals = super()._create_vals(vals)
        vals.update({
            'customer': True,
        })
        vals.update({
            'type': self._name,
        })
        return vals

    @api.model_cr_context
    def _get_default_image_path(self, vals):
        res = super()._get_default_image_path(vals)
        if res:
            return res
        image_path = get_module_resource(
            'clv_address', 'static/src/img', 'address-avatar.png',
        )
        return image_path

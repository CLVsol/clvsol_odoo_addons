# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.modules import get_module_resource


class Family(models.Model):

    _name = 'clv.family'
    _description = 'Family'
    _inherit = 'clv.abstract.partner_entity'

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            if record.code:
                result.append(
                    (record.id,
                     u'%s [%s]' % (record.name, record.code)
                     ))
            else:
                result.append(
                    (record.id,
                     u'%s' % (record.name)
                     ))
        return result

    code = fields.Char(string='Family Code', required=False)

    @api.model
    def _create_vals(self, vals):
        vals = super()._create_vals(vals)
        vals.update({
            'customer': True,
        })
        return vals

    @api.model_cr_context
    def _get_default_image_path(self, vals):
        res = super()._get_default_image_path(vals)
        if res:
            return res
        image_path = get_module_resource(
            'clv_family', 'static/src/img', 'family-avatar.png',
        )
        return image_path

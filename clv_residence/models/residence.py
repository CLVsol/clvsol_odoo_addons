# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models
from odoo.modules import get_module_resource

_logger = logging.getLogger(__name__)


class Residence(models.Model):

    _name = 'clv.residence'
    _description = 'Residence'
    _inherit = 'clv.abstract.partner_entity'

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

    code = fields.Char(string='Residence Code', required=False)

    notes = fields.Text(string='Notes:')

    @api.model
    def _create_vals(self, vals):
        vals = super()._create_vals(vals)
        vals.update({
            'type': self._name,
        })
        return vals

    def _get_default_image_path(self, vals):
        res = super()._get_default_image_path(vals)
        if res:
            return res
        image_path = get_module_resource(
            'clv_residence', 'static/src/img', 'residence-avatar.png',
        )
        return image_path

    def write(self, values):
        ret = super().write(values)
        for record in self:
            if ('code' in values):
                if record.entity_code != values['code']:
                    vals = {}
                    vals['entity_code'] = values['code']
                    super().write(vals)
        return ret

    def do_residence_clear_address_data(self):

        for address_aux in self:

            data_values = {}

            data_values['street_name'] = False
            data_values['street2'] = False
            data_values['zip'] = False
            data_values['city'] = False
            data_values['state_id'] = False
            data_values['country_id'] = False
            # data_values['phone'] = False
            # data_values['mobile'] = False

            _logger.info(u'>>>>>>>>>> %s', data_values)

            address_aux.write(data_values)

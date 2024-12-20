# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PartnerEntityStreetPattern(models.Model):
    _description = 'Partner Entity Street Pattern'
    _name = "clv.partner_entity.street_pattern"
    _order = "street, street2"
    _rec_name = 'street'

    @api.depends('street', 'street2')
    def name_get(self):
        result = []
        for record in self:
            if record.street2:
                result.append(
                    (record.id,
                     u'%s (%s)' % (record.street, record.street2)
                     ))
            else:
                result.append(
                    (record.id,
                     u'%s' % (record.street)
                     ))
        return result

    street = fields.Char(string='Street')

    street2 = fields.Char(string='Street 2')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('pattern_uniq',
         'UNIQUE(street, street2)',
         u'Error! The Pattern must be unique!'
         ),
    ]

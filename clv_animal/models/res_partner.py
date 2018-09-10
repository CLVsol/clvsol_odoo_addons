# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[
        ('clv.animal', 'Animal'),
    ])

    animal_ids = fields.One2many(
        string='Related Animals',
        comodel_name='clv.animal',
        compute='_compute_animal_ids_and_count',
    )
    count_animals = fields.Integer(
        compute='_compute_animal_ids_and_count',
    )

    @api.multi
    def _get_clv_entity(self):
        self.ensure_one()
        if self.type and self.type[:3] == 'clv':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    @api.multi
    def _compute_animal_ids_and_count(self):
        for record in self:
            animals = self.env['clv.animal'].search([
                ('partner_id', 'child_of', record.id),
            ])
            record.count_animals = len(animals)
            record.animal_ids = [(6, 0, animals.ids)]

    @api.model
    def create(self, vals):
        """ It overrides create to bind appropriate clv entity. """
        if all((
            vals.get('type', '').startswith('clv.'),
            not self.env.context.get('clv_entity_no_create'),
        )):
            model = self.env[vals['type']].with_context(
                clv_entity_no_create=True,
            )
            clv_entity = model.create(vals)
            return clv_entity.partner_id
        return super(ResPartner, self).create(vals)

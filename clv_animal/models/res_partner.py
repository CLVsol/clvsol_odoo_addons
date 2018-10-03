# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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

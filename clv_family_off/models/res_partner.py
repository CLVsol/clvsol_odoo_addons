# -*- coding: utf-8 -*-
# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    type = fields.Selection(selection_add=[
        ('clv.family_off', 'Family (Off)'),
    ])
    family_off_ids = fields.One2many(
        string='Related Families (Off)',
        comodel_name='clv.family_off',
        compute='_compute_family_off_ids_and_count',
    )
    count_families = fields.Integer(
        compute='_compute_family_off_ids_and_count',
    )

    @api.multi
    def _get_clv_entity(self):
        self.ensure_one()
        if self.type and self.type[:3] == 'clv':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    @api.multi
    def _compute_family_off_ids_and_count(self):
        for record in self:
            family_offs = self.env['clv.family_off'].search([
                ('partner_id', 'child_of', record.id),
            ])
            record.count_families = len(family_offs)
            record.family_off_ids = [(6, 0, family_offs.ids)]

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
        return super().create(vals)

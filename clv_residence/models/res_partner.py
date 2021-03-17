# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[
        ('clv.residence', 'Residence'),
    ])

    residence_ids = fields.One2many(
        string='Related Residences',
        comodel_name='clv.residence',
        compute='_compute_residence_ids_and_count',
    )
    count_residences = fields.Integer(
        compute='_compute_residence_ids_and_count',
    )

    def _get_clv_entity(self):
        self.ensure_one()
        if self.type and self.type[:3] == 'clv':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    def _compute_residence_ids_and_count(self):
        for record in self:
            try:
                residences = self.env['clv.residence'].search([
                    ('partner_id', 'child_of', record.id),
                ])
                record.count_residences = len(residences)
                record.residence_ids = [(6, 0, residences.ids)]
            except TypeError:
                record.count_residences = False
                record.residence_ids = False

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    residence_ids = fields.One2many(
        comodel_name='clv.residence',
        inverse_name='phase_id',
        string='Residences',
        readonly=True
    )
    count_residences = fields.Integer(
        string='Residences (count)',
        compute='_compute_residence_ids_and_count',
    )

    def _compute_residence_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            residences = self.env['clv.residence'].search(search_domain)

            record.count_residences = len(residences)
            record.residence_ids = [(6, 0, residences.ids)]


class Family(models.Model):
    _inherit = 'clv.residence'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )

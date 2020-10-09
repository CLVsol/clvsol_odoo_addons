# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    family_history_ids = fields.One2many(
        comodel_name='clv.family.history',
        inverse_name='phase_id',
        string='Families (History)',
        readonly=True
    )
    count_family_histories = fields.Integer(
        string='Families (History) (count)',
        compute='_compute_family_history_ids_and_count',
    )

    def _compute_family_history_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            family_histories = self.env['clv.family.history'].search(search_domain)

            record.count_family_histories = len(family_histories)
            record.family_history_ids = [(6, 0, family_histories.ids)]


class FamilyHistory(models.Model):
    _inherit = 'clv.family.history'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )

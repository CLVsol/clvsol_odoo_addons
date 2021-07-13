# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    residence_history_ids = fields.One2many(
        comodel_name='clv.residence.history',
        inverse_name='phase_id',
        string='Residences (History)',
        readonly=True
    )
    count_residence_histories = fields.Integer(
        string='Residences (History) (count)',
        compute='_compute_residence_history_ids_and_count',
    )

    def _compute_residence_history_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            residence_histories = self.env['clv.residence.history'].search(search_domain)

            record.count_residence_histories = len(residence_histories)
            record.residence_history_ids = [(6, 0, residence_histories.ids)]


class ResidenceHistory(models.Model):
    _inherit = 'clv.residence.history'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )

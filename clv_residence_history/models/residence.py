# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResidenceHistory(models.Model):
    _inherit = 'clv.residence.history'

    residence_id = fields.Many2one(
        comodel_name='clv.residence',
        string='Residence',
        ondelete='restrict'
    )


class Residence(models.Model):
    _inherit = 'clv.residence'

    residence_history_ids = fields.One2many(
        comodel_name='clv.residence.history',
        inverse_name='residence_id',
        string='Residences (History)'
    )
    count_residence_histories = fields.Integer(
        string='Residences (History) (count)',
        compute='_compute_count_residence_histories',
    )

    @api.depends('residence_history_ids')
    def _compute_count_residence_histories(self):
        for r in self:
            r.count_residence_histories = len(r.residence_history_ids)

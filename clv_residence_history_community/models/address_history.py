# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressHistory(models.Model):
    _inherit = 'clv.address.history'

    is_residence_history = fields.Boolean(
        string='Is Residence History',
        default=False
    )

    residence_history_ids = fields.One2many(
        comodel_name='clv.residence.history',
        inverse_name='related_address_history_id',
        string='Residence Histories'
    )
    count_residence_histories = fields.Integer(
        string='Residence Histories (count)',
        compute='_compute_count_residence_histories',
        store=False
    )

    def _compute_count_residence_histories(self):
        for r in self:
            r.count_residence_histories = len(r.residence_history_ids)


class ResidenceHistory(models.Model):
    _inherit = 'clv.residence.history'

    related_address_history_is_unavailable = fields.Boolean(
        string='Related Address History is unavailable',
        default=True,
    )
    related_address_history_id = fields.Many2one(
        comodel_name='clv.address.history',
        string='Related Address',
        ondelete='restrict')

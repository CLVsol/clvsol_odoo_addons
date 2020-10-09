# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Phase(models.Model):
    _inherit = 'clv.phase'

    address_history_ids = fields.One2many(
        comodel_name='clv.address.history',
        inverse_name='phase_id',
        string='Addresses (History)',
        readonly=True
    )
    count_address_histories = fields.Integer(
        string='Addresses (History) (count)',
        compute='_compute_address_history_ids_and_count',
    )

    def _compute_address_history_ids_and_count(self):
        for record in self:

            search_domain = [
                ('phase_id', '=', record.id),
            ]

            address_histories = self.env['clv.address.history'].search(search_domain)

            record.count_address_histories = len(address_histories)
            record.address_history_ids = [(6, 0, address_histories.ids)]


class AddressHistory(models.Model):
    _inherit = 'clv.address.history'

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase',
        ondelete='restrict'
    )

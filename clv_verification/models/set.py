# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class VerificationSchedule(models.Model):
    _inherit = 'clv.verification.schedule'

    verification_set_elements = fields.Boolean(string='Verification Set Elements', default=False)

    verification_set_id = fields.Many2one(
        comodel_name='clv.set',
        string='Set',
        ondelete='restrict'
    )
    count_verification_set_elements = fields.Integer(
        string='Set Elements (count)',
        compute='_compute_count_verification_set_elements',
        store=False
    )

    @api.depends('verification_set_id')
    def _compute_count_verification_set_elements(self):
        for r in self:
            r.count_verification_set_elements = len(r.verification_set_id.set_element_ids)

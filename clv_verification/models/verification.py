# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Verification(models.Model):
    _description = 'Verification'
    _name = 'clv.verification'
    _inherit = 'clv.abstract.verification'
    _order = "id desc"
    _rec_name = 'verification_reference_name'

    verification_model = fields.Char(string='Model Name ', required=True)
    verification_res_id = fields.Integer(
        string='Record ID',
        help="ID of the target record in the database"
    )
    verification_reference = fields.Char(
        string='Reference ',
        compute='_compute_verification_reference',
        readonly=True,
        store=True
    )
    verification_reference_name = fields.Char(
        string='Reference Name',
        compute='_compute_verification_reference',
        readonly=True,
        store=True
    )

    @api.depends('verification_model', 'verification_res_id')
    def _compute_verification_reference(self):
        for record in self:
            if (record.verification_model is not False) and (record.verification_res_id != 0):
                record.verification_reference = "%s,%s" % (record.verification_model,
                                                           record.verification_res_id)
                Model = self.env[record.verification_model]
                rec = Model.search([
                    ('id', '=', record.verification_res_id),
                ])
                record.verification_reference_name = rec.name_get()[0][1]

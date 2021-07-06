# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Residence(models.Model):
    _inherit = 'clv.residence'

    patient_history_ids = fields.One2many(
        comodel_name='clv.patient.history',
        inverse_name='ref_residence_id',
        string='Persons (History)'
    )
    count_patient_histories = fields.Integer(
        string='Persons (History) (count)',
        compute='_compute_count_patient_historiess',
    )

    @api.depends('patient_history_ids')
    def _compute_count_patient_historiess(self):
        for r in self:
            r.count_patient_histories = len(r.patient_history_ids)


class PersonHistory(models.Model):
    _inherit = 'clv.patient.history'

    ref_residence_id = fields.Many2one(
        comodel_name='clv.residence',
        string='Residence',
        ondelete='restrict'
    )

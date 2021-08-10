# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PersonHistory(models.Model):
    _inherit = 'clv.person.history'

    is_patient_history = fields.Boolean(
        string='Is Patient History',
        default=False
    )

    patient_history_ids = fields.One2many(
        comodel_name='clv.patient.history',
        inverse_name='related_person_history_id',
        string='Patient Histories'
    )
    count_patient_histories = fields.Integer(
        string='Patient Histories (count)',
        compute='_compute_count_patient_histories',
        store=False
    )

    def _compute_count_patient_histories(self):
        for r in self:
            r.count_patient_histories = len(r.patient_history_ids)


class PatientHistory(models.Model):
    _inherit = 'clv.patient.history'

    related_person_history_is_unavailable = fields.Boolean(
        string='Related Person History is unavailable',
        default=True,
    )
    related_person_history_id = fields.Many2one(
        comodel_name='clv.person.history',
        string='Related Person',
        ondelete='restrict')

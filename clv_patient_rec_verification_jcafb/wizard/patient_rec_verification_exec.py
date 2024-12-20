# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class PatientRecVerificationExecute(models.TransientModel):
    _description = 'Patient (Rec) Verification Execute'
    _name = 'clv.patient_rec.verification_exec'

    def _default_patient_rec_ids(self):
        return self._context.get('active_ids')
    patient_rec_ids = fields.Many2many(
        comodel_name='clv.patient_rec',
        relation='clv_patient_rec_verification_outcome_refresh_rel',
        string='Patients (Rec)',
        default=_default_patient_rec_ids)
    count_patients_aux = fields.Integer(
        string='Number of Patients (Rec)',
        compute='_compute_count_patients_aux',
        store=False
    )

    @api.depends('patient_rec_ids')
    def _compute_count_patients_aux(self):
        for r in self:
            r.count_patients_aux = len(r.patient_rec_ids)

    def do_patient_rec_verification_exec(self):
        self.ensure_one()

        for patient_rec in self.patient_rec_ids:

            patient_rec._patient_rec_verification_exec()

        return True

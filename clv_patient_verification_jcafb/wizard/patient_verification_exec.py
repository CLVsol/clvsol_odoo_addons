# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class PatientVerificationExecute(models.TransientModel):
    _description = 'Patient Verification Execute'
    _name = 'clv.patient.verification_exec'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_verification_outcome_refresh_rel',
        string='Patients',
        default=_default_patient_ids)
    count_patients = fields.Integer(
        string='Number of Patients',
        compute='_compute_count_patients',
        store=False
    )

    @api.depends('patient_ids')
    def _compute_count_patients(self):
        for r in self:
            r.count_patients = len(r.patient_ids)

    def do_patient_verification_exec(self):
        self.ensure_one()

        for patient in self.patient_ids:

            patient._patient_verification_exec()

        return True

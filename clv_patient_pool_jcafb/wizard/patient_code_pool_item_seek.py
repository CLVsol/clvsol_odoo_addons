# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientCodePoolSeek(models.TransientModel):
    _description = 'Patient Code Pool Seek'
    _name = 'clv.patient.code_pool.item_seek'

    def _default_patient_code_pool_ids(self):
        return self._context.get('active_ids')
    patient_code_pool_ids = fields.Many2many(
        comodel_name='clv.patient.code_pool',
        relation='clv_patient_code_pool_patient_code_pool_item_seek_rel',
        string='Patient Code Pools',
        default=_default_patient_code_pool_ids
    )

    def do_patient_code_pool_item_seek(self):
        self.ensure_one()

        PatientCodePoolItem = self.env['clv.patient.code_pool.item']
        Patient = self.env['clv.patient']

        for patient_code_pool in self.patient_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', patient_code_pool.name)

            search_domain = [
                ('patient_code_pool_id', '=', patient_code_pool.id),
            ]
            items = PatientCodePoolItem.search(search_domain)

            for item in items:

                if (item.patient_id is not False):

                    item.patient_id = False

            for item in items:

                patients = Patient.search([])

                for patient in patients:

                    if (patient.code == item.code):

                        item.patient_id = patient.id

        return True

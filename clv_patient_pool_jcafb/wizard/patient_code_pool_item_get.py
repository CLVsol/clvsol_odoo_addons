# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientCodePoolGet(models.TransientModel):
    _description = 'Patient Code Pool Get'
    _name = 'clv.patient.code_pool.item_get'

    def _default_patient_code_pool_ids(self):
        return self._context.get('active_ids')
    patient_code_pool_ids = fields.Many2many(
        comodel_name='clv.patient.code_pool',
        relation='clv_patient_code_pool_patient_code_pool_item_get_rel',
        string='Patient Code Pools',
        default=_default_patient_code_pool_ids
    )

    def do_patient_code_pool_item_get(self):
        self.ensure_one()

        PatientCodePoolItem = self.env['clv.patient.code_pool.item']
        Patient = self.env['clv.patient']

        for patient_code_pool in self.patient_code_pool_ids:

            _logger.info(u'%s %s', '>>>>>', patient_code_pool.name)

            patients = Patient.search([])
            items = PatientCodePoolItem.search([])

            for patient in patients:

                found_item = False
                for item in items:

                    if (patient.code == item.code):
                        found_item = True

                if not found_item:

                    if patient.code is not False:

                        sequence_str = patient.code[:7].replace('.', '')
                        format_code = self.env['clv.abstract.code'].format_code(sequence_str)

                        if patient.code == format_code:

                            values = {
                                'patient_code_pool_id': patient_code_pool.id,
                                'code_sequence': patient_code_pool.code_sequence,
                                'code': patient.code,
                                'patient_id': patient.id,
                                'notes': 'New'
                            }

                        else:

                            values = {
                                'patient_code_pool_id': patient_code_pool.id,
                                'code_sequence': patient_code_pool.code_sequence,
                                'code': patient.code,
                                'patient_id': patient.id,
                                'notes': 'New (Invalid)'
                            }

                        patient_code_pool_item = PatientCodePoolItem.create(values)

                        _logger.info(u'%s %s - %s', '>>>>>>>>>>', patient_code_pool_item.code, patient_code_pool_item.notes)

        return True

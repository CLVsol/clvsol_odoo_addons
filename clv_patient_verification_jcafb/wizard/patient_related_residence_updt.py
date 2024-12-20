# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientResidenceUpdt(models.TransientModel):
    _description = 'Patient Residence Update'
    _name = 'clv.patient.residence_updt'

    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_residence_updt_rel',
        string='Patients',
        default=_default_patient_ids
    )

    residence_verification_exec = fields.Boolean(
        string='Residence Verification Execute',
        default=True,
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute',
        default=True,
    )

    def do_patient_residence_updt(self):
        self.ensure_one()

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if not patient.residence_is_unavailable:

                residence = patient.residence_id
                vals = {}

                if (patient.state != residence.state):

                    vals['state'] = patient.state

                if (patient.phase_id != residence.phase_id):

                    vals['phase_id'] = patient.phase_id.id

                if (patient.employee_id != residence.employee_id):

                    vals['employee_id'] = patient.employee_id.id

                # if self.update_contact_info_data:
                if True:

                    # if (patient.contact_info_is_unavailable != residence.contact_info_is_unavailable):

                    #     vals['contact_info_is_unavailable'] = patient.contact_info_is_unavailable

                    if (patient.zip != residence.zip):

                        vals['zip'] = patient.zip

                    if (patient.street_name != residence.street_name):

                        vals['street_name'] = patient.street_name

                    if (patient.street_number != residence.street_number):

                        vals['street_number'] = patient.street_number

                    if (patient.street_number2 != residence.street_number2):

                        vals['street_number2'] = patient.street_number2

                    if (patient.street2 != residence.street2):

                        vals['street2'] = patient.street2

                    if (patient.country_id != residence.country_id):

                        vals['country_id'] = patient.country_id.id

                    if (patient.state_id != residence.state_id):

                        vals['state_id'] = patient.state_id.id

                    if (patient.city_id != residence.city_id):

                        vals['city_id'] = patient.city_id.id

                if vals != {}:

                    vals['reg_state'] = 'revised'

                _logger.info(u'%s %s', '>>>>>>>>>>', vals)
                residence.write(vals)

            if self.residence_verification_exec:
                if patient.residence_id.id is not False:
                    patient.residence_id._residence_verification_exec()

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Residence(models.Model):
    _inherit = 'clv.residence'

    patient_ids = fields.One2many(
        comodel_name='clv.patient',
        inverse_name='residence_id',
        string='Patients'
    )
    count_patients = fields.Integer(
        string='Patients (count)',
        compute='_compute_count_patients',
        # store=True
    )

    # @api.depends('patient_ids')
    def _compute_count_patients(self):
        for r in self:
            r.count_patients = len(r.patient_ids)


class Patient(models.Model):
    _inherit = 'clv.patient'

    residence_is_unavailable = fields.Boolean(
        string='Residence is unavailable',
        default=True,
    )
    residence_id = fields.Many2one(comodel_name='clv.residence', string='Residence', ondelete='restrict')
    residence_code = fields.Char(string='Residence Code', related='residence_id.code', store=False)

    residence_category_ids = fields.Char(
        string='Residence Categories',
        related='residence_id.category_ids.name',
        store=True
    )

    residence_state = fields.Selection(
        string='Residence State',
        related='residence_id.state',
        store=False
    )

    def do_patient_get_residence_data(self):

        for patient in self:

            _logger.info(u'>>>>> %s', patient.residence_id)

            if (patient.residence_id.id is not False):

                data_values = {}

                if patient.residence_id.id is not False:

                    data_values['street_name'] = patient.residence_id.street_name
                    data_values['street_number'] = patient.residence_id.street_number
                    data_values['street_number2'] = patient.residence_id.street_number2
                    data_values['street2'] = patient.residence_id.street2
                    data_values['zip'] = patient.residence_id.zip
                    data_values['city'] = patient.residence_id.city
                    data_values['city_id'] = patient.residence_id.city_id.id
                    data_values['state_id'] = patient.residence_id.state_id.id
                    data_values['country_id'] = patient.residence_id.country_id.id

                    data_values['phone'] = patient.residence_id.phone
                    data_values['mobile'] = patient.residence_id.mobile
                    data_values['email'] = patient.residence_id.email

                _logger.info(u'>>>>>>>>>> %s', data_values)

                patient.write(data_values)

        return True

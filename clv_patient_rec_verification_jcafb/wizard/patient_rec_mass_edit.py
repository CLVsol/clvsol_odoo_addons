# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PatientRecMassEdit(models.TransientModel):
    _inherit = 'clv.patient_rec.mass_edit'

    contact_info_is_unavailable = fields.Boolean(
        string='Contact Information is unavailable'
    )
    contact_info_is_unavailable_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Contact Information is unavailable:', default=False, readonly=False, required=False
    )
    clear_address_data = fields.Boolean(
        string='Clear Address Data'
    )

    verification_marker_ids = fields.Many2many(
        comodel_name='clv.verification.marker',
        relation='clv_patient_rec_mass_edit_verification_marker_rel',
        column1='patient_rec_id',
        column2='verification_marker_id',
        string='Verification Markers'
    )
    verification_marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Verification Markers:', default=False, readonly=False, required=False
    )

    patient_rec_verification_exec = fields.Boolean(
        string='Patient (Rec) Verification Execute'
    )

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        value = self.env['clv.default_value'].search([
            ('model', '=', 'clv.patient_rec'),
            ('parameter', '=', 'mass_edit_patient_rec_verification_exec'),
            ('enabled', '=', True),
        ]).value
        patient_rec_verification_exec = False
        if value == 'True':
            patient_rec_verification_exec = True

        defaults['patient_rec_verification_exec'] = patient_rec_verification_exec

        return defaults

    def do_patient_rec_mass_edit(self):
        self.ensure_one()

        super().do_patient_rec_mass_edit()

        for patient_rec in self.patient_rec_ids:

            _logger.info(u'%s %s', '>>>>>', patient_rec.name)

            if self.contact_info_is_unavailable_selection == 'set':
                patient_rec.contact_info_is_unavailable = self.contact_info_is_unavailable
            if self.contact_info_is_unavailable_selection == 'remove':
                patient_rec.contact_info_is_unavailable = False

            if self.clear_address_data:
                patient_rec.do_patient_rec_clear_address_data()

            if self.verification_marker_ids_selection == 'add':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_rec.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_rec.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'set':
                m2m_list = []
                for verification_marker_id in patient_rec.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_rec.verification_marker_ids = m2m_list
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_rec.verification_marker_ids = m2m_list

            if self.patient_rec_verification_exec:
                patient_rec._patient_rec_verification_exec()

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientMassEdit(models.TransientModel):
    _inherit = 'clv.patient.mass_edit'

    residence_is_unavailable = fields.Boolean(
        string='Residence is unavailable'
    )
    residence_is_unavailable_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Residence is unavailable:', default=False, readonly=False, required=False
    )

    residence_id = fields.Many2one(
        comodel_name='clv.residence',
        string='Residence'
    )
    residence_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Residence:', default=False, readonly=False, required=False
    )

    verification_marker_ids = fields.Many2many(
        comodel_name='clv.verification.marker',
        relation='clv_patient_mass_edit_verification_marker_rel',
        column1='patient_id',
        column2='verification_marker_id',
        string='Verification Markers'
    )
    verification_marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Verification Markers:', default=False, readonly=False, required=False
    )

    patient_verification_exec = fields.Boolean(
        string='Patient Verification Execute'
    )

    def do_patient_mass_edit(self):
        self.ensure_one()

        super().do_patient_mass_edit()

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if self.residence_is_unavailable_selection == 'set':
                patient.residence_is_unavailable = self.residence_is_unavailable
            if self.residence_is_unavailable_selection == 'remove':
                patient.residence_is_unavailable = False

            if self.residence_id_selection == 'set':
                patient.residence_id = self.residence_id.id
            if self.residence_id_selection == 'remove':
                patient.residence_id = False

            if self.verification_marker_ids_selection == 'add':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'set':
                m2m_list = []
                for verification_marker_id in patient.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.verification_marker_ids = m2m_list
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.verification_marker_ids = m2m_list

            if self.patient_verification_exec:
                patient._patient_verification_exec()

        return True

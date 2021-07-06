# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PatientHistoryPatientMassEdit(models.TransientModel):
    _description = 'Patient History - Patient Mass Edit'
    _name = 'clv.patient.history.patient_mass_edit'

    def _default_patient_history_ids(self):
        return self._context.get('active_ids')
    patient_history_ids = fields.Many2many(
        comodel_name='clv.patient.history',
        relation='clv_patient_history_patient_mass_edit_rel',
        string='Patient Histories',
        default=_default_patient_history_ids
    )

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_patient_history_patient_mass_edit_global_tag_rel',
        column1='patient_id',
        column2='global_tag_id',
        string='Global Tags'
    )
    global_tag_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Global Tags:', default=False, readonly=False, required=False
    )

    category_ids = fields.Many2many(
        comodel_name='clv.patient.category',
        relation='clv_patient_history_patient_mass_edit_category_rel',
        column1='patient_id',
        column2='category_id',
        string='Categories'
    )
    category_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Categories:', default=False, readonly=False, required=False
    )

    marker_ids = fields.Many2many(
        comodel_name='clv.patient.marker',
        relation='clv_patient_history_patient_mass_edit_marker_rel',
        column1='patient_id',
        column2='marker_id',
        string='Markers'
    )
    marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Markers:', default=False, readonly=False, required=False
    )

    tag_ids = fields.Many2many(
        comodel_name='clv.patient.tag',
        relation='clv_patient_history_patient_mass_edit_tag_rel',
        column1='patient_id',
        column2='tag_id',
        string='Patient Tags'
    )
    tag_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Patient Tags:', default=False, readonly=False, required=False
    )

    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    def do_patient_history_patient_mass_edit(self):
        self.ensure_one()

        Patient = self.env['clv.patient']

        for patient_history in self.patient_history_ids:

            patient = Patient.search([
                ('id', '=', patient_history.patient_id.id),
            ])

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if self.global_tag_ids_selection == 'add':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'set':
                m2m_list = []
                for global_tag_id in patient.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.global_tag_ids = m2m_list
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.global_tag_ids = m2m_list

            if self.category_ids_selection == 'add':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.category_ids = m2m_list
            if self.category_ids_selection == 'remove_m2m':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.category_ids = m2m_list
            if self.category_ids_selection == 'set':
                m2m_list = []
                for category_id in patient.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.category_ids = m2m_list
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.category_ids = m2m_list

            if self.marker_ids_selection == 'add':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list
            if self.marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list
            if self.marker_ids_selection == 'set':
                m2m_list = []
                for marker_id in patient.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.marker_ids = m2m_list

            if self.tag_ids_selection == 'add':
                m2m_list = []
                for tag_id in self.tag_ids:
                    m2m_list.append((4, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.tag_ids = m2m_list
            if self.tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for tag_id in self.tag_ids:
                    m2m_list.append((3, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.tag_ids = m2m_list
            if self.tag_ids_selection == 'set':
                m2m_list = []
                for tag_id in patient.tag_ids:
                    m2m_list.append((3, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.tag_ids = m2m_list
                m2m_list = []
                for tag_id in self.tag_ids:
                    m2m_list.append((4, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient.tag_ids = m2m_list

        return True

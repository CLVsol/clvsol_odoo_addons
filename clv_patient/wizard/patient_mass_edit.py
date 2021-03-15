# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

'''
Reference: http://help.odoo.com/question/18704/hide-menu-for-existing-group/

There are actually0-6 numbers for representing each job for a many2many/ one2many field

    (0, 0, { values }) -- link to a new record that needs to be created with the given values dictionary
    (1, ID, { values }) -- update the linked record with id = ID (write values on it)
    (2, ID) -- remove and delete the linked record with id = ID (calls unlink on ID, that will delete the
               object completely, and the link to it as well)
    (3, ID) -- cut the link to the linked record with id = ID (delete the relationship between the two
               objects but does not delete the target object itself)
    (4, ID) -- link to existing record with id = ID (adds a relationship)
    (5) -- unlink all (like using (3,ID) for all linked records)
    (6, 0, [IDs]) -- replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
'''

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PatientMassEdit(models.TransientModel):
    _description = 'Patient Mass Edit'
    _name = 'clv.patient.mass_edit'

    # patient_ids = fields.Many2many(
    #     comodel_name='clv.patient',
    #     relation='clv_patient_mass_edit_rel',
    #     string='Patients'
    # )
    def _default_patient_ids(self):
        return self._context.get('active_ids')
    patient_ids = fields.Many2many(
        comodel_name='clv.patient',
        relation='clv_patient_mass_edit_rel',
        string='Patients',
        default=_default_patient_ids
    )

    reg_state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
         ('done', 'Done'),
         ('canceled', 'Canceled')
         ], string='Register State', default=False, readonly=False, required=False
    )
    reg_state_selection = fields.Selection(
        [('set', 'Set'),
         ], string='Register State:', default=False, readonly=False, required=False
    )

    state = fields.Selection(
        [('new', 'New'),
         ('available', 'Available'),
         ('waiting', 'Waiting'),
         ('selected', 'Selected'),
         ('unselected', 'Unselected'),
         ('unavailable', 'Unavailable'),
         ('unknown', 'Unknown')
         ], string='State', default=False, readonly=False, required=False
    )
    state_selection = fields.Selection(
        [('set', 'Set'),
         ], string='State:', default=False, readonly=False, required=False
    )

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_patient_mass_edit_global_tag_rel',
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
        relation='clv_patient_mass_edit_category_rel',
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
        relation='clv_patient_mass_edit_marker_rel',
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

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible Empĺoyee'
    )
    employee_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Responsible Empĺoyee:', default=False, readonly=False, required=False
    )

    random_field = fields.Char(
        string='Random ID', default=False,
        help='Use "/" to get an automatic new Random ID.'
    )
    random_field_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Random ID:', default=False, readonly=False, required=False
    )

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase'
    )
    phase_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Phase:', default=False, readonly=False, required=False
    )

    tag_ids = fields.Many2many(
        comodel_name='clv.patient.tag',
        relation='clv_patient_mass_edit_tag_rel',
        column1='patient_id',
        column2='tag_id',
        string='Patient Tag'
    )
    tag_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Patient Tag:', default=False, readonly=False, required=False
    )

    partner_entity_code_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Partner Entity Code:', default=False, readonly=False, required=False
    )

    patient_ref_age_refresh = fields.Boolean(
        string='Patient Reference Age Refresh'
    )

    active_log = fields.Boolean(
        string='Active Log'
    )
    active_log_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Active Log:', default=False, readonly=False, required=False
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

    @api.model
    def default_get(self, field_names):

        defaults = super().default_get(field_names)

        # defaults['patient_ids'] = self.env.context['active_ids']

        return defaults

    def do_patient_mass_edit(self):
        self.ensure_one()

        for patient in self.patient_ids:

            _logger.info(u'%s %s', '>>>>>', patient.name)

            if self.reg_state_selection == 'set':
                patient.reg_state = self.reg_state
            if self.reg_state_selection == 'remove':
                patient.reg_state = False

            if self.state_selection == 'set':
                patient.state = self.state
            if self.state_selection == 'remove':
                patient.state = False

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

            if self.employee_id_selection == 'set':
                patient.employee_id = self.employee_id
            if self.employee_id_selection == 'remove':
                patient.employee_id = False

            if self.random_field_selection == 'set':
                patient.random_field = self.random_field
            if self.random_field_selection == 'remove':
                patient.random_field = False

            if self.phase_id_selection == 'set':
                patient.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                patient.phase_id = False

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

            if self.partner_entity_code_selection == 'set':
                if patient.entity_code != patient.code:
                    vals = {}
                    vals['entity_code'] = patient.code
                    patient.write(vals)
            if self.partner_entity_code_selection == 'remove':
                if patient.entity_code is not False:
                    vals = {}
                    vals['entity_code'] = False
                    patient.write(vals)

            if self.patient_ref_age_refresh:
                patient._compute_age_reference()
                patient._compute_age_range_id()

            if self.active_log_selection == 'set':
                patient.active_log = self.active_log
            if self.active_log_selection == 'remove':
                patient.active_log = False

        return True

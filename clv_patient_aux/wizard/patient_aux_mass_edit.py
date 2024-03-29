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


class PatientAuxMassEdit(models.TransientModel):
    _description = 'Patient (Aux) Mass Edit'
    _name = 'clv.patient_aux.mass_edit'

    # patient_aux_ids = fields.Many2many(
    #     comodel_name='clv.patient_aux',
    #     relation='clv_patient_aux_mass_edit_rel',
    #     string='Patients (Aux)'
    # )
    def _default_patient_aux_ids(self):
        return self._context.get('active_ids')
    patient_aux_ids = fields.Many2many(
        comodel_name='clv.patient_aux',
        relation='clv_patient_aux_mass_edit_rel',
        string='Patients (Aux)',
        default=_default_patient_aux_ids
    )

    reg_state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
         ('verified', 'Verified'),
         ('ready', 'Ready'),
         ('done', 'Done'),
         ('canceled', 'Canceled')
         ], string='Register State', readonly=False, required=False
    )
    reg_state_selection = fields.Selection(
        [('set', 'Set'),
         ], string='Register State:', readonly=False, required=False
    )

    state = fields.Selection(
        [('new', 'New'),
         ('available', 'Available'),
         ('waiting', 'Waiting'),
         ('selected', 'Selected'),
         ('unselected', 'Unselected'),
         ('unavailable', 'Unavailable'),
         ('unknown', 'Unknown')
         ], string='State', readonly=False, required=False
    )
    state_selection = fields.Selection(
        [('set', 'Set'),
         ], string='State:', readonly=False, required=False
    )

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_patient_aux_mass_edit_global_tag_rel',
        column1='patient_aux_id',
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
        relation='clv_patient_aux_mass_edit_category_rel',
        column1='patient_aux_id',
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
        relation='clv_patient_aux_mass_edit_marker_rel',
        column1='patient_aux_id',
        column2='marker_id',
        string='Markers'
    )
    marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Markers:', default=False, readonly=False, required=False
    )

    phase_id = fields.Many2one(
        comodel_name='clv.phase',
        string='Phase'
    )
    phase_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Phase:', readonly=False, required=False
    )

    partner_entity_code_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Partner Entity Code:', default=False, readonly=False, required=False
    )

    patient_aux_ref_age_refresh = fields.Boolean(
        string='Patient (Aux) Reference Age Refresh'
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

        # defaults['patient_aux_ids'] = self.env.context['active_ids']

        param_value = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip()
        phase_id = False
        if param_value:
            phase_id = int(param_value)

        phase_id_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.patient_aux'),
            ('parameter', '=', 'mass_edit_phase_id_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['phase_id'] = phase_id
        defaults['phase_id_selection'] = phase_id_selection

        reg_state = self.env['clv.default_value'].search([
            ('model', '=', 'clv.patient_aux'),
            ('parameter', '=', 'mass_edit_reg_state'),
            ('enabled', '=', True),
        ]).value

        reg_state_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.patient_aux'),
            ('parameter', '=', 'mass_edit_reg_state_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['reg_state'] = reg_state
        defaults['reg_state_selection'] = reg_state_selection

        state = self.env['clv.default_value'].search([
            ('model', '=', 'clv.patient_aux'),
            ('parameter', '=', 'mass_edit_state'),
            ('enabled', '=', True),
        ]).value

        state_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.patient_aux'),
            ('parameter', '=', 'mass_edit_state_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['state'] = state
        defaults['state_selection'] = state_selection

        return defaults

    def do_patient_aux_mass_edit(self):
        self.ensure_one()

        for patient_aux in self.patient_aux_ids:

            _logger.info(u'%s %s', '>>>>>', patient_aux.name)

            if self.reg_state_selection == 'set':
                patient_aux.reg_state = self.reg_state
            if self.reg_state_selection == 'remove':
                patient_aux.reg_state = False

            if self.state_selection == 'set':
                patient_aux.state = self.state
            if self.state_selection == 'remove':
                patient_aux.state = False

            if self.global_tag_ids_selection == 'add':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'set':
                m2m_list = []
                for global_tag_id in patient_aux.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.global_tag_ids = m2m_list
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.global_tag_ids = m2m_list

            if self.category_ids_selection == 'add':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.category_ids = m2m_list
            if self.category_ids_selection == 'remove_m2m':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.category_ids = m2m_list
            if self.category_ids_selection == 'set':
                m2m_list = []
                for category_id in patient_aux.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.category_ids = m2m_list
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.category_ids = m2m_list

            if self.marker_ids_selection == 'add':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.marker_ids = m2m_list
            if self.marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.marker_ids = m2m_list
            if self.marker_ids_selection == 'set':
                m2m_list = []
                for marker_id in patient_aux.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.marker_ids = m2m_list
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                patient_aux.marker_ids = m2m_list

            if self.phase_id_selection == 'set':
                patient_aux.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                patient_aux.phase_id = False

            if self.partner_entity_code_selection == 'set':
                if patient_aux.entity_code != patient_aux.code:
                    vals = {}
                    vals['entity_code'] = patient_aux.code
                    patient_aux.write(vals)
            if self.partner_entity_code_selection == 'remove':
                if patient_aux.entity_code is not False:
                    vals = {}
                    vals['entity_code'] = False
                    patient_aux.write(vals)

            if self.patient_aux_ref_age_refresh:
                patient_aux._compute_age_reference()
                patient_aux._compute_age_range_id()

            if self.active_log_selection == 'set':
                patient_aux.active_log = self.active_log
            if self.active_log_selection == 'remove':
                patient_aux.active_log = False

        return True

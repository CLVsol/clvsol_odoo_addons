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


class FamilyMassEdit(models.TransientModel):
    _description = 'Family Mass Edit'
    _name = 'clv.family.mass_edit'

    family_ids = fields.Many2many(
        comodel_name='clv.family',
        relation='clv_family_mass_edit_rel',
        string='Families'
    )

    reg_state = fields.Selection(
        [('draft', 'Draft'),
         ('revised', 'Revised'),
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
        relation='clv_family_mass_edit_global_tag_rel',
        column1='family_id',
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
        comodel_name='clv.family.category',
        relation='clv_family_mass_edit_category_rel',
        column1='family_id',
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
        comodel_name='clv.family.marker',
        relation='clv_family_mass_edit_marker_rel',
        column1='family_id',
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

    tag_ids = fields.Many2many(
        comodel_name='clv.family.tag',
        relation='clv_family_mass_edit_tag_rel',
        column1='family_id',
        column2='tag_id',
        string='Family Tags'
    )
    tag_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Family Tags:', default=False, readonly=False, required=False
    )

    partner_entity_code_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Partner Entity Code:', default=False, readonly=False, required=False
    )

    automatic_set_name = fields.Boolean(
        string='Automatic Name'
    )
    automatic_set_name_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Automatic Name:', default=False, readonly=False, required=False
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

        defaults['family_ids'] = self.env.context['active_ids']

        param_value = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip()
        phase_id = False
        if param_value:
            phase_id = int(param_value)

        phase_id_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.family'),
            ('parameter', '=', 'mass_edit_phase_id_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['phase_id'] = phase_id
        defaults['phase_id_selection'] = phase_id_selection

        reg_state = self.env['clv.default_value'].search([
            ('model', '=', 'clv.family'),
            ('parameter', '=', 'mass_edit_reg_state'),
            ('enabled', '=', True),
        ]).value

        reg_state_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.family'),
            ('parameter', '=', 'mass_edit_reg_state_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['reg_state'] = reg_state
        defaults['reg_state_selection'] = reg_state_selection

        state = self.env['clv.default_value'].search([
            ('model', '=', 'clv.family'),
            ('parameter', '=', 'mass_edit_state'),
            ('enabled', '=', True),
        ]).value

        state_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.family'),
            ('parameter', '=', 'mass_edit_state_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['state'] = state
        defaults['state_selection'] = state_selection

        return defaults

    def do_family_mass_edit(self):
        self.ensure_one()

        for family in self.family_ids:

            _logger.info(u'%s %s', '>>>>>', family.name)

            if self.reg_state_selection == 'set':
                family.reg_state = self.reg_state
            if self.reg_state_selection == 'remove':
                family.reg_state = False

            if self.state_selection == 'set':
                family.state = self.state
            if self.state_selection == 'remove':
                family.state = False

            if self.global_tag_ids_selection == 'add':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'set':
                m2m_list = []
                for global_tag_id in family.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.global_tag_ids = m2m_list
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.global_tag_ids = m2m_list

            if self.category_ids_selection == 'add':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.category_ids = m2m_list
            if self.category_ids_selection == 'remove_m2m':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.category_ids = m2m_list
            if self.category_ids_selection == 'set':
                m2m_list = []
                for category_id in family.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.category_ids = m2m_list
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.category_ids = m2m_list

            if self.marker_ids_selection == 'add':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.marker_ids = m2m_list
            if self.marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.marker_ids = m2m_list
            if self.marker_ids_selection == 'set':
                m2m_list = []
                for marker_id in family.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.marker_ids = m2m_list
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.marker_ids = m2m_list

            if self.phase_id_selection == 'set':
                family.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                family.phase_id = False

            if self.tag_ids_selection == 'add':
                m2m_list = []
                for tag_id in self.tag_ids:
                    m2m_list.append((4, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.tag_ids = m2m_list
            if self.tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for tag_id in self.tag_ids:
                    m2m_list.append((3, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.tag_ids = m2m_list
            if self.tag_ids_selection == 'set':
                m2m_list = []
                for tag_id in family.tag_ids:
                    m2m_list.append((3, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.tag_ids = m2m_list
                m2m_list = []
                for tag_id in self.tag_ids:
                    m2m_list.append((4, tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                family.tag_ids = m2m_list

            if self.partner_entity_code_selection == 'set':
                if family.entity_code != family.code:
                    vals = {}
                    vals['entity_code'] = family.code
                    family.write(vals)
            if self.partner_entity_code_selection == 'remove':
                if family.entity_code is not False:
                    vals = {}
                    vals['entity_code'] = False
                    family.write(vals)

            if self.automatic_set_name_selection == 'set':
                family.automatic_set_name = self.automatic_set_name
            if self.automatic_set_name_selection == 'remove':
                family.automatic_set_name = False

            if self.active_log_selection == 'set':
                family.active_log = self.active_log
            if self.active_log_selection == 'remove':
                family.active_log = False

        return True

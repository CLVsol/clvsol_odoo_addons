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


class AddressAuxMassEdit(models.TransientModel):
    _description = 'Address (Aux) Mass Edit'
    _name = 'clv.address_aux.mass_edit'

    address_aux_ids = fields.Many2many(
        comodel_name='clv.address_aux',
        relation='clv_address_aux_mass_edit_rel',
        string='Addresses (Aux)'
    )

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_address_aux_mass_edit_global_tag_rel',
        column1='address_aux_id',
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
        comodel_name='clv.address.category',
        relation='clv_address_aux_mass_edit_category_rel',
        column1='address_aux_id',
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
        comodel_name='clv.address.marker',
        relation='clv_address_aux_mass_edit_marker_rel',
        column1='address_aux_id',
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

        defaults['address_aux_ids'] = self.env.context['active_ids']

        param_value = self.env['ir.config_parameter'].sudo().get_param(
            'clv.global_settings.current_phase_id', '').strip()
        phase_id = False
        if param_value:
            phase_id = int(param_value)

        phase_id_selection = self.env['clv.default_value'].search([
            ('model', '=', 'clv.address_aux'),
            ('parameter', '=', 'mass_edit_phase_id_selection'),
            ('enabled', '=', True),
        ]).value

        defaults['phase_id'] = phase_id
        defaults['phase_id_selection'] = phase_id_selection

        return defaults

    def do_address_aux_mass_edit(self):
        self.ensure_one()

        for address_aux in self.address_aux_ids:

            _logger.info(u'%s %s', '>>>>>', address_aux.name)

            if self.global_tag_ids_selection == 'add':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'remove_m2m':
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.global_tag_ids = m2m_list
            if self.global_tag_ids_selection == 'set':
                m2m_list = []
                for global_tag_id in address_aux.global_tag_ids:
                    m2m_list.append((3, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.global_tag_ids = m2m_list
                m2m_list = []
                for global_tag_id in self.global_tag_ids:
                    m2m_list.append((4, global_tag_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.global_tag_ids = m2m_list

            if self.category_ids_selection == 'add':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.category_ids = m2m_list
            if self.category_ids_selection == 'remove_m2m':
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.category_ids = m2m_list
            if self.category_ids_selection == 'set':
                m2m_list = []
                for category_id in address_aux.category_ids:
                    m2m_list.append((3, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.category_ids = m2m_list
                m2m_list = []
                for category_id in self.category_ids:
                    m2m_list.append((4, category_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.category_ids = m2m_list

            if self.marker_ids_selection == 'add':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.marker_ids = m2m_list
            if self.marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.marker_ids = m2m_list
            if self.marker_ids_selection == 'set':
                m2m_list = []
                for marker_id in address_aux.marker_ids:
                    m2m_list.append((3, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.marker_ids = m2m_list
                m2m_list = []
                for marker_id in self.marker_ids:
                    m2m_list.append((4, marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.marker_ids = m2m_list

            if self.phase_id_selection == 'set':
                address_aux.phase_id = self.phase_id
            if self.phase_id_selection == 'remove':
                address_aux.phase_id = False

            if self.partner_entity_code_selection == 'set':
                if address_aux.entity_code != address_aux.code:
                    vals = {}
                    vals['entity_code'] = address_aux.code
                    address_aux.write(vals)
            if self.partner_entity_code_selection == 'remove':
                if address_aux.entity_code is not False:
                    vals = {}
                    vals['entity_code'] = False
                    address_aux.write(vals)

            if self.automatic_set_name_selection == 'set':
                address_aux.automatic_set_name = self.automatic_set_name
            if self.automatic_set_name_selection == 'remove':
                address_aux.automatic_set_name = False

            if self.active_log_selection == 'set':
                address_aux.active_log = self.active_log
            if self.active_log_selection == 'remove':
                address_aux.active_log = False

        return True

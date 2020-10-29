# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class GlobalLogCrientMassEdit(models.TransientModel):
    _description = 'Global Log Crient Mass Edit'
    _name = 'clv.global_log.client.mass_edit'

    def _default_global_log_client_ids(self):
        return self._context.get('active_ids')
    global_log_client_ids = fields.Many2many(
        comodel_name='clv.global_log.client',
        relation='clv_global_log_client_mass_edit_rel',
        string='Global Log Clients',
        default=_default_global_log_client_ids
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

    # @api.model
    # def default_get(self, field_names):

    #     defaults = super().default_get(field_names)

    #     defaults['global_log_client_ids'] = self.env.context['active_ids']

    #     return defaults

    def do_global_log_client_mass_edit(self):
        self.ensure_one()

        for global_log_client in self.global_log_client_ids:

            _logger.info(u'%s %s', '>>>>>', global_log_client.model_name)

            Model = self.env[global_log_client.model_name]

            if self.active_log_selection == 'set':

                model_instances = Model.search([('active_log', '!=', self.active_log)])

                for model_instance in model_instances:
                    model_instance.active_log = self.active_log

                self.env.cr.commit()
                _logger.info(u'%s %s', '>>>>>>>>>>', len(model_instances))

            if self.active_log_selection == 'remove':

                model_instances = Model.search([('active_log', '!=', False)])

                for model_instance in model_instances:
                    model_instance.active_log = False

                self.env.cr.commit()
                _logger.info(u'%s %s', '>>>>>>>>>>', len(model_instances))

        return True

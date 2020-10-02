# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInputMassEdit(models.TransientModel):
    _description = 'Survey User Input Mass Edit'
    _name = 'survey.user_input.mass_edit'

    def _default_survey_user_input_ids(self):
        return self._context.get('active_ids')
    survey_user_input_ids = fields.Many2many(
        comodel_name='survey.user_input',
        relation='survey_user_input_mass_edit_rel',
        string='Survey User Inputs',
        default=_default_survey_user_input_ids
    )

    state = fields.Selection(
        [('new', 'Not started yet'),
         ('in_progress', 'Partially completed'),
         ('done', 'Completed')
         ], string='Status', default=False, readonly=False, required=False
    )
    state_selection = fields.Selection(
        [('set', 'Set'),
         ], string='Status:', default=False, readonly=False, required=False
    )

    reset_last_displayed_page = fields.Boolean(
        string='Reset Last Displayed Page',
        default=True,
        readonly=False
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

    def do_survey_user_input_mass_edit(self):
        self.ensure_one()

        for survey_user_input in self.survey_user_input_ids:

            _logger.info(u'%s %s', '>>>>>', survey_user_input.access_token)

            if self.state_selection == 'set':
                survey_user_input.state = self.state
            if self.state_selection == 'remove':
                survey_user_input.state = False

            if self.reset_last_displayed_page:
                survey_user_input.last_displayed_page_id = False

        return True

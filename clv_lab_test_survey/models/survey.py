# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from werkzeug import urls

from odoo import fields, models


class LabTestResult(models.Model):
    _inherit = 'clv.lab_test.result'

    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string='Survey Type')
    survey_user_input_id = fields.Many2one(
        comodel_name='survey.user_input',
        string='Survey User Input'
    )
    survey_user_input_state = fields.Selection(
        string='Survey User Input State',
        related='survey_user_input_id.state',
        store=False
    )
    survey_user_input_state_2 = fields.Selection(
        string='Survey User Input State 2',
        related='survey_user_input_id.state_2',
        store=False
    )

    survey_url = fields.Char(
        string='Survey URL',
        compute="_compute_survey_url"
    )

    def _compute_survey_url(self):

        base_url = '/' if self.env.context.get('relative_url') else \
                   self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for lab_test_result in self:
            user_input = lab_test_result.survey_user_input_id
            lab_test_result.survey_url = \
                urls.url_join(
                    base_url, "survey/%s/%s" % (user_input.survey_id.access_token, user_input.access_token))

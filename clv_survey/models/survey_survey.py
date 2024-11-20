# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from werkzeug import urls

from odoo import fields, models
from odoo import exceptions


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'
    _order = 'title'

    code = fields.Char(string='Survey Code', required=False)

    public_url = fields.Char("Public link", compute="_compute_survey_url")

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Survey Code must be unique!'),
    ]

    def copy(self):
        raise exceptions.ValidationError('It is not possible to duplicate the record, please create a new one.')

    def _compute_survey_url(self):
        """ Computes a public URL for the survey """
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for survey in self:
            survey.public_url = urls.url_join(base_url, "survey/start/%s" % (survey.access_token))

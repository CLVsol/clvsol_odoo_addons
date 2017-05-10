# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveyCodeUpdate(models.TransientModel):
    _name = 'clv.survey.code_updt'

    def _default_survey_ids(self):
        return self._context.get('active_ids')
    survey_ids = fields.Many2many(
        comodel_name='survey.survey',
        relation='clv_survey_code_updt_rel',
        string='Surveys',
        default=_default_survey_ids
    )

    @api.multi
    def do_survey_code_updt(self):
        self.ensure_one()

        ir_model_data_model = self.env['ir.model.data']

        for survey_reg in self.survey_ids:

            ir_model_data_search = ir_model_data_model.search([
                ('model', '=', 'survey.survey'),
                ('res_id', '=', survey_reg.id)
            ])

            for ir_model_data_reg in ir_model_data_search:
                if survey_reg.code is False:
                    _logger.info(u'%s %s %s', '>>>>>', survey_reg.code, ir_model_data_reg.name)
                    survey_reg.code = ir_model_data_reg.name

            for survey_page_reg in survey_reg.page_ids:

                ir_model_data_search = ir_model_data_model.search([
                    ('model', '=', 'survey.page'),
                    ('res_id', '=', survey_page_reg.id)
                ])

                for ir_model_data_reg in ir_model_data_search:
                    if survey_page_reg.code is False:
                        _logger.info(u'%s %s %s', '>>>>>>>>>>', survey_page_reg.code, ir_model_data_reg.name)
                        survey_page_reg.code = ir_model_data_reg.name

                for survey_question_reg in survey_page_reg.question_ids:

                    ir_model_data_search = ir_model_data_model.search([
                        ('model', '=', 'survey.question'),
                        ('res_id', '=', survey_question_reg.id)
                    ])

                    for ir_model_data_reg in ir_model_data_search:
                        if survey_question_reg.code is False:
                            _logger.info(u'%s %s %s',
                                         '>>>>>>>>>>>>>>>', survey_question_reg.code, ir_model_data_reg.name)
                            survey_question_reg.code = ir_model_data_reg.name

                    for survey_label_reg in survey_question_reg.labels_ids:

                        ir_model_data_search = ir_model_data_model.search([
                            ('model', '=', 'survey.label'),
                            ('res_id', '=', survey_label_reg.id)
                        ])

                        for ir_model_data_reg in ir_model_data_search:
                            if survey_label_reg.code is False:
                                _logger.info(u'%s %s %s',
                                             '>>>>>>>>>>>>>>>>>>>>', survey_label_reg.code, ir_model_data_reg.name)
                                survey_label_reg.code = ir_model_data_reg.name

                    for survey_label_reg in survey_question_reg.labels_ids_2:

                        ir_model_data_search = ir_model_data_model.search([
                            ('model', '=', 'survey.label'),
                            ('res_id', '=', survey_label_reg.id)
                        ])

                        for ir_model_data_reg in ir_model_data_search:
                            if survey_label_reg.code is False:
                                _logger.info(u'%s %s %s',
                                             '>>>>>>>>>>>>>>>>>>>>', survey_label_reg.code, ir_model_data_reg.name)
                                survey_label_reg.code = ir_model_data_reg.name

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DocumentSurveyUserInputValidate(models.TransientModel):
    _description = 'Survey User Input Validate'
    _name = 'clv.document.survey_user_input_validate'

    def _default_document_ids(self):
        return self._context.get('active_ids')
    document_ids = fields.Many2many(
        comodel_name='clv.document',
        relation='clv_document_survey_user_input_validate_rel',
        string='Documents',
        default=_default_document_ids
    )

    survey_user_input_reflesh_exec = fields.Boolean(
        string='Survey User Input Refresh Execute',
        default=True
    )

    def do_document_survey_user_input_validate(self):
        self.ensure_one()

        for document in self.document_ids:

            if self.survey_user_input_reflesh_exec:
                document.survey_user_input_id._survey_user_input_refresh()

            document.survey_user_input_id._survey_user_input_validate()

        return True

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class DocumentSurveyUserInputSetInProgress(models.TransientModel):
    _description = 'Survey User Input Set In Progress'
    _name = 'clv.document.survey_user_input_set_in_progress'

    def _default_document_ids(self):
        return self._context.get('active_ids')
    document_ids = fields.Many2many(
        comodel_name='clv.document',
        relation='clv_document_survey_user_input_set_in_progress_rel',
        string='Documents',
        default=_default_document_ids
    )

    def do_document_survey_user_input_set_in_progress(self):
        self.ensure_one()

        for document in self.document_ids:

            if document.survey_user_input_id.id is not False:

                document.survey_user_input_id.state = 'in_progress'
                document.survey_user_input_id.state_2 = 'returned'

                document.reg_state = 'revised'
                document.state = 'returned'

        return True

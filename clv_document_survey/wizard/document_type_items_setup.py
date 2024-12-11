# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class DocumentTypeItemsSetUp(models.TransientModel):
    _inherit = 'clv.document.type.items_setup'

    def _do_document_type_items_setup(self, document_type):
        self.ensure_one()

        Survey = self.env['survey.survey']
        SurveyQuestion = self.env['survey.question']
        DocumentItem = self.env['clv.document.item']

        survey = Survey.search([
            ('code', '=', document_type.code),
        ])

        _logger.info(u'%s %s', '>>>>>>>>>>', survey.code)

        document_items = DocumentItem.search([
            ('document_type_id', '=', document_type.id),
        ])
        document_items.unlink()

        items = []
        sequence = 0

        pages = SurveyQuestion.search([
            ('survey_id', '=', survey.id),
            ('is_page', '=', True),
        ])

        for page in pages:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', page.code)

            _title_ = page.title.encode("utf-8")

            sequence += 1
            items.append((0, 0, {'code': page.code,
                                 'name': _title_,
                                 'sequence': sequence,
                                 }))

            for question in page.question_ids:

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>', question.code)

                question_type = question.question_type
                # _question_ = question.question.encode("utf-8")
                _question_ = question.title.encode("utf-8")

                sequence += 1
                items.append((0, 0, {'code': question.code,
                                     'name': _question_,
                                     'sequence': sequence,
                                     }))

                if question.comments_allowed is True:

                    if question.comments_message is not False:
                        _comments_message_ = question.comments_message.encode("utf-8")

                    sequence += 1
                    items.append((0, 0, {'code': question.code + '_C',
                                         'name': _comments_message_,
                                         'sequence': sequence,
                                         }))

                if question_type == 'free_text' or question_type == 'textbox' or question_type == 'datetime':
                    pass

                if question_type == 'simple_choice':
                    pass

                if question_type == 'multiple_choice':
                    pass

                if question_type == 'matrix':

                    # for label in question.labels_ids_2:
                    for label in question.matrix_row_ids:

                        _value_ = label.value.encode("utf-8")

                        sequence += 1
                        items.append((0, 0, {'code': label.code,
                                             'name': _value_,
                                             'sequence': sequence,
                                             }))

        document_type.item_ids = items

        return True

    def do_document_type_items_setup(self):
        self.ensure_one()

        super().do_document_type_items_setup()

        for document_type in self.document_type_ids:

            _logger.info(u'%s %s', '>>>>>', document_type.code)

            self._do_document_type_items_setup(document_type)

        return True

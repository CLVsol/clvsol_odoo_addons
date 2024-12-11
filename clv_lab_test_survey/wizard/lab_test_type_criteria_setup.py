# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class DocumentTypeCriteriaSetUp(models.TransientModel):
    _inherit = 'clv.lab_test.type.criteria_setup'

    def _do_lab_test_type_criteria_setup(self, lab_test_type):
        self.ensure_one()

        Survey = self.env['survey.survey']
        SurveyQuestion = self.env['survey.question']
        LabTestCriterion = self.env['clv.lab_test.criterion']

        survey = Survey.search([
            ('code', '=', lab_test_type.code),
        ])

        _logger.info(u'%s %s', '>>>>>>>>>>', survey.code)

        lab_test_criteria = LabTestCriterion.search([
            ('lab_test_type_id', '=', lab_test_type.id),
        ])
        lab_test_criteria.unlink()

        criteria = []
        sequence = 0

        pages = SurveyQuestion.search([
            ('survey_id', '=', survey.id),
            ('is_page', '=', True),
        ])

        for page in pages:

            _logger.info(u'%s %s', '>>>>>>>>>>>>>>>', page.code)

            _title_ = page.title.encode("utf-8")

            sequence += 1
            criteria.append((0, 0, {'code': page.code,
                                    'name': _title_,
                                    'sequence': sequence,
                                    }))

            for question in page.question_ids:

                _logger.info(u'%s %s', '>>>>>>>>>>>>>>>>>>>>', question.code)

                question_type = question.question_type
                # _question_ = question.question.encode("utf-8")
                _question_ = question.title.encode("utf-8")

                sequence += 1
                criteria.append((0, 0, {'code': question.code,
                                        'name': _question_,
                                        'sequence': sequence,
                                        }))

                if question.comments_allowed is True:

                    if question.comments_message is not False:
                        _comments_message_ = question.comments_message.encode("utf-8")

                    sequence += 1
                    criteria.append((0, 0, {'code': question.code + '_C',
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

                    for label in question.labels_ids_2:

                        _value_ = label.value.encode("utf-8")

                        sequence += 1
                        criteria.append((0, 0, {'code': label.code,
                                                'name': _value_,
                                                'sequence': sequence,
                                                }))

        lab_test_type.criterion_ids = criteria

        return True

    def do_lab_test_type_criteria_setup(self):
        self.ensure_one()

        super().do_lab_test_type_criteria_setup()

        for lab_test_type in self.lab_test_type_ids:

            _logger.info(u'%s %s', '>>>>>', lab_test_type.code)

            self._do_lab_test_type_criteria_setup(lab_test_type)

        return True

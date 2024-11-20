# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class QuestionLabelSetUp(models.TransientModel):
    _description = 'Question Label SetUp'
    _name = 'survey.question.label_setup'

    question_ids = fields.Many2many(
        comodel_name='survey.question',
        relation='survey_question_label_setup_rel',
        string='Questions'
    )

    clear_current_labels = fields.Boolean(string='Clear Current Labels')

    use_set_elements = fields.Boolean(string='Use Set Elements')

    set_id = fields.Many2one(
        comodel_name='clv.set',
        string='Set',
        ondelete='restrict'
    )
    count_set_elements = fields.Integer(
        string='Set Elements (count)',
        compute='_compute_count_set_elements',
        store=False
    )

    @api.depends('set_id')
    def _compute_count_set_elements(self):
        for r in self:
            r.count_set_elements = len(r.set_id.set_element_ids)

    @api.model
    def default_get(self, field_names):

        defaults = super(QuestionLabelSetUp, self).default_get(field_names)

        defaults['question_ids'] = self.env.context['active_ids']
        _logger.info(u'%s %s', '>>>>>>>>>>', self.env.context['active_ids'])

        defaults['use_set_elements'] = False

        return defaults

    def do_question_label_setup(self):
        self.ensure_one()

        for ref_question in self.question_ids:

            _logger.info(u'%s %s %s %s', '>>>>>', ref_question.code, ref_question.title, ref_question.description)

            _logger.info(u'%s %s', '>>>>>>>>>>', ref_question.question_type)

            SurveyLabel = self.env['survey.label']
            if self.clear_current_labels:
                labels = SurveyLabel.search([
                    ('question_id', '=', ref_question.id),
                ])
                for label in labels:
                    label.unlink()

            labels = SurveyLabel.search([
                ('question_id', '=', ref_question.id),
            ])
            sequence = 0
            for label in labels:
                if label.sequence > sequence:
                    sequence = label.sequence

            for set_element in self.set_id.set_element_ids:

                sequence += 1
                values = {
                    'value': set_element.ref_id.name_get()[0][1],
                    'question_id': ref_question.id,
                    'sequence': sequence,
                }
                SurveyLabel.create(values)

        return True

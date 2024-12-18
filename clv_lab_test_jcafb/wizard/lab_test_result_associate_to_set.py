# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class LabTestResultAssociateToSet(models.TransientModel):
    _description = 'Lab Test Result Associate to Set'
    _name = 'clv.lab_test.result.associate_to_set'

    def _default_lab_test_result_ids(self):
        return self._context.get('active_ids')
    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_associate_to_set_rel',
        string='Lab Test Results',
        default=_default_lab_test_result_ids
    )

    create_new_set = fields.Boolean(string='Create new Set', default=False)

    set_id = fields.Many2one(
        comodel_name='clv.set',
        string='Set',
        required=False
    )

    set_name = fields.Char(string='Set Name', required=False, help="Set Name")

    def do_lab_test_result_associate_to_set(self):
        self.ensure_one()

        Set = self.env['clv.set']
        SetElement = self.env['clv.set.element']

        actual_set = False

        if self.create_new_set:

            if self.set_name is False:
                raise UserError(u'"Set Name" can not be null!')

            else:

                actual_set = Set.search([
                    ('name', '=', self.set_name),
                ])
                _logger.info(u'%s %s %s', '>>>>>>>>>>', 'actual_set_id:', actual_set.id)

                if actual_set.id is False:

                    values = {}
                    values['name'] = self.set_name
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                    actual_set = Set.create(values)
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', 'actual_set:', actual_set)

        else:

            if self.set_id.id is False:
                raise UserError(u'"Set" can not be null!')

            else:

                actual_set = self.set_id
                _logger.info(u'%s %s %s', '>>>>>>>>>>', 'actual_set:', actual_set)

        lab_test_result_count = 0
        for lab_test_result in self.lab_test_result_ids:

            lab_test_result_count += 1

            _logger.info(u'%s %s %s', '>>>>>', lab_test_result_count, lab_test_result.display_name)

            set_element = SetElement.search([
                ('set_id', '=', actual_set.id),
                ('ref_id', '=', lab_test_result._name + ',' + str(lab_test_result.id)),
            ])

            if set_element.id is False:

                values = {}
                values['set_id'] = actual_set.id
                values['ref_id'] = lab_test_result._name + ',' + str(lab_test_result.id)
                _logger.info(u'%s %s %s', '>>>>>>>>>>', 'values:', values)
                new_set_element = SetElement.create(values)
                _logger.info(u'%s %s %s', '>>>>>>>>>>', 'new_set_element:', new_set_element)

        return True

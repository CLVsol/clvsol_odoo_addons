# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestResult(models.Model):
    _description = 'Lab Test Result'
    _name = "clv.lab_test.result"
    _rec_name = 'code'
    _order = 'code'

    code = fields.Char(string='Lab Test Result Code')

    lab_test_type_id = fields.Many2one(comodel_name='clv.lab_test.type', string='Lab Test Type')
    lab_test_type_code = fields.Char(string='Lab Test Type Code', related='lab_test_type_id.code', store=False)
    lab_test_request_id = fields.Many2one(comodel_name='clv.lab_test.request', string='Lab Test Request')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    lab_test_result_ids = fields.One2many(
        comodel_name='clv.lab_test.result',
        inverse_name='lab_test_type_id',
        string='Lab Test Results'
    )


class LabTestRequest(models.Model):
    _inherit = 'clv.lab_test.request'

    lab_test_result_ids = fields.One2many(
        comodel_name='clv.lab_test.result',
        inverse_name='lab_test_request_id',
        string='Lab Test Results'
    )

    count_lab_test_results = fields.Integer(
        string='Lab Test Results (count)',
        compute='_compute_lab_test_result_ids_and_count',
    )
    count_lab_test_results_2 = fields.Integer(
        string='Lab Test Results 2 (count)',
        compute='_compute_lab_test_result_ids_and_count',
    )

    def _compute_lab_test_result_ids_and_count(self):
        for record in self:

            search_domain = [
                ('lab_test_request_id', '=', record.id),
            ]
            lab_test_results_2 = self.env['clv.lab_test.result'].search(search_domain)

            lab_test_results = self.env['clv.lab_test.result'].search(search_domain)

            record.count_lab_test_results = len(lab_test_results)
            record.count_lab_test_results_2 = len(lab_test_results_2)
            record.lab_test_result_ids = [(6, 0, lab_test_results.ids)]

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestReport(models.Model):
    _description = 'Lab Test Report'
    _name = "clv.lab_test.report"
    _rec_name = 'code'
    _order = 'code'

    code = fields.Char(string='Lab Test Report Code')

    lab_test_type_id = fields.Many2one(comodel_name='clv.lab_test.type', string='Lab Test Type')
    lab_test_type_code = fields.Char(string='Lab Test Type Code', related='lab_test_type_id.code', store=False)
    lab_test_request_id = fields.Many2one(comodel_name='clv.lab_test.request', string='Lab Test Request')
    lab_test_result_id = fields.Many2one(comodel_name='clv.lab_test.result', string='Lab Test Result')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    lab_test_report_ids = fields.One2many(
        comodel_name='clv.lab_test.report',
        inverse_name='lab_test_type_id',
        string='Lab Test Reports'
    )


class LabTestRequest(models.Model):
    _inherit = 'clv.lab_test.request'

    lab_test_report_ids = fields.One2many(
        comodel_name='clv.lab_test.report',
        inverse_name='lab_test_request_id',
        string='Lab Test Reports'
    )

    count_lab_test_reports = fields.Integer(
        string='Lab Test Reports (count)',
        compute='_compute_lab_test_report_ids_and_count',
    )
    count_lab_test_reports_2 = fields.Integer(
        string='Lab Test Reports 2 (count)',
        compute='_compute_lab_test_report_ids_and_count',
    )

    def _compute_lab_test_report_ids_and_count(self):
        for record in self:

            search_domain = [
                ('lab_test_request_id', '=', record.id),
            ]
            lab_test_reports_2 = self.env['clv.lab_test.report'].search(search_domain)

            lab_test_reports = self.env['clv.lab_test.report'].search(search_domain)

            record.count_lab_test_reports = len(lab_test_reports)
            record.count_lab_test_reports_2 = len(lab_test_reports_2)
            record.lab_test_report_ids = [(6, 0, lab_test_reports.ids)]


class LabTestResult(models.Model):
    _inherit = 'clv.lab_test.result'

    lab_test_report_ids = fields.One2many(
        comodel_name='clv.lab_test.report',
        inverse_name='lab_test_result_id',
        string='Lab Test Reports'
    )

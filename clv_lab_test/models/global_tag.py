# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class GlobalTag(models.Model):
    _inherit = 'clv.global_tag'

    lab_test_result_ids = fields.Many2many(
        comodel_name='clv.lab_test.result',
        relation='clv_lab_test_result_global_tag_rel',
        column1='global_tag_id',
        column2='lab_test_result_id',
        string='Lab Test Results'
    )


class LabTestResult(models.Model):
    _inherit = 'clv.lab_test.result'

    global_tag_ids = fields.Many2many(
        comodel_name='clv.global_tag',
        relation='clv_lab_test_result_global_tag_rel',
        column1='lab_test_result_id',
        column2='global_tag_id',
        string='Global Tags'
    )
    global_tag_names = fields.Char(
        string='Global Tag Names',
        compute='_compute_global_tag_names',
        store=True
    )

    @api.depends('global_tag_ids')
    def _compute_global_tag_names(self):
        for r in self:
            global_tag_names = False
            for global_tag in r.global_tag_ids:
                if global_tag_names is False:
                    global_tag_names = global_tag.name
                else:
                    global_tag_names = global_tag_names + ', ' + global_tag.name
            r.global_tag_names = global_tag_names

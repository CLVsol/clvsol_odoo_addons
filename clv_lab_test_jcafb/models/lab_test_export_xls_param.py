# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, fields, models


class LabTestTypeExportXlsParam(models.Model):
    _description = 'Lab Test Export XLS Parameter'
    _name = "clv.lab_test.export_xls.param"

    lab_test_type_id = fields.Many2one(comodel_name='clv.lab_test.type', string='Test Type')

    display = fields.Selection(
        [('none', 'None'),
         ('result', 'Result'),
         ('report', 'Report')
         ], string='Display', default='none', readonly=False, required=True
    )

    parameter_type = fields.Selection(
        [('constant_char', 'Constant Char'),
         ('constant_int', 'Constant Integer'),
         ('constant_float', 'Constant Float'),
         ('image_file_name', 'Image File Name'),
         ('expression', 'Expression'),
         ('result_code', 'Result Code'),
         ('variable_name', 'Variable Name')
         ], string='Parameter Type', default='variable_name', readonly=False, required=True
    )

    parameter = fields.Char(string='Parameter')

    cell = fields.Char(string='Cell')

    col_nr = fields.Integer(string='Column Number')
    row_nr = fields.Integer(string='Row Number')

    active = fields.Boolean(string='Active', default=1)

    suggested_col_nr = fields.Char(
        string="Suggested Column Number", required=False, store=True,
        compute="_get_suggested_col_row_nr",
        help='Suggested Column Number for the Cell.'
    )
    suggested_row_nr = fields.Char(
        string="Suggested Row Number", required=False, store=True,
        compute="_get_suggested_col_row_nr",
        help='Suggested Row Number for the Cell.'
    )

    def col_to_num(self, col_str):
        """ Convert base26 column string to number. """
        expn = 0
        col_num = 0
        for char in reversed(col_str):
            col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
            expn += 1

        return col_num

    @api.depends('cell')
    def _get_suggested_col_row_nr(self):
        for record in self:
            if record.cell:
                res = re.findall('(\d+|[A-Za-z]+)', record.cell)
                record.suggested_col_nr = self.col_to_num(res[0]) - 1
                record.suggested_row_nr = int(res[1]) - 1

    # @api.model
    @api.model_create_multi
    # def create(self, values):
    def create(self, vals_list):
        # record = super().create(values)

        # if record.row_nr != record.suggested_row_nr:
        #     record['row_nr'] = record.suggested_row_nr

        # if record.col_nr != record.suggested_col_nr:
        #     record['col_nr'] = record.suggested_col_nr

        # return record
        for values in vals_list:
            values = self._create_vals(values)
        record = super().create(values)

        if record.row_nr != record.suggested_row_nr:
            record['row_nr'] = record.suggested_row_nr

        if record.col_nr != record.suggested_col_nr:
            record['col_nr'] = record.suggested_col_nr

        return record

    def write(self, values):
        ret = super().write(values)

        for record in self:

            if record.suggested_row_nr is not False:
                if record.row_nr != record.suggested_row_nr:
                    values['row_nr'] = record.suggested_row_nr
                    super().write(values)

            if record.suggested_col_nr is not False:
                if record.col_nr != record.suggested_col_nr:
                    values['col_nr'] = record.suggested_col_nr
                    super().write(values)

        return ret


class LabTestType(models.Model):
    _inherit = 'clv.lab_test.type'

    lab_test_export_xls_param_ids = fields.One2many(
        comodel_name='clv.lab_test.export_xls.param',
        inverse_name='lab_test_type_id',
        string='Lab Test Export XLS Parameters'
    )

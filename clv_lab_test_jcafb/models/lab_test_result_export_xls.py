# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook

from datetime import timedelta

# from os import listdir
# from os.path import isfile, join, exists, normpath, realpath
import os.path
from PIL import Image

from odoo import models

_logger = logging.getLogger(__name__)


class LabTestResult(models.Model):
    _name = "clv.lab_test.result"
    _inherit = 'clv.lab_test.result'

    def lab_test_result_export_xls(self, dir_path, file_name, use_template, template_dir_path):

        lab_test_type = self.lab_test_type_id.code
        # lab_test_request_code = self.lab_test_request_id.code
        lab_test_result_code = self.code

        FileSystemDirectory = self.env['clv.file_system.directory']
        file_system_directory = FileSystemDirectory.search([
            ('directory', '=', dir_path),
        ])

        if use_template:
            template_file_name = self.lab_test_type_id.template_file_name_result
            template_file_path = template_dir_path + '/' + template_file_name
            book = open_workbook(template_file_path, formatting_info=True)
            wbook = copy(book)
            sheet = wbook.get_sheet(0)
            # file_name = file_name.replace('<type>', lab_test_type).replace('<request_code>', lab_test_request_code)
            file_name = file_name.replace('<type>', lab_test_type).replace('<result_code>', lab_test_result_code)
            file_path = dir_path + '/' + file_name
            idx = book.sheet_names().index(template_file_name)
            wbook.get_sheet(idx).name = file_name
        else:
            # file_name = file_name.replace('<type>', lab_test_type).replace('<request_code>', lab_test_request_code)
            file_name = file_name.replace('<type>', lab_test_type).replace('<result_code>', lab_test_result_code)
            file_path = dir_path + '/' + file_name
            wbook = xlwt.Workbook()
            sheet = wbook.add_sheet(file_name)

        delta_hours = -3

        lab_test_type_id = self.lab_test_type_id.id
        reference_name = self.ref_id.name
        reference_code = self.ref_id.code
        # received_by_name = self.lab_test_request_id.employee_id.name
        # received_by_code = self.lab_test_request_id.employee_id.code
        received_by_name = self.employee_id_request.name
        received_by_code = self.employee_id_request.code
        # date_received = (self.lab_test_request_id.date_received + timedelta(hours=delta_hours)).strftime('%d-%m-%Y  %H:%M:%S')
        date_received = (self.date_received + timedelta(hours=delta_hours)).strftime('%d-%m-%Y  %H:%M:%S')

        # _logger.info(u'%s %s %s %s', '>>>>>>>>>>', lab_test_request_code, lab_test_type, use_template)
        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', lab_test_result_code, lab_test_type, use_template)

        save_book = False

        ExportXLS = self.env['clv.export_xls']

        LabTestTypeExportXlsParam = self.env['clv.lab_test.export_xls.param']

        parameters = LabTestTypeExportXlsParam.search([
            ('lab_test_type_id', '=', lab_test_type_id),
            ('display', '=', 'result'),
            ('parameter_type', '=', 'image_file_name'),
        ])

        for parameter in parameters:

            # image_file_path = template_dir_path + '/' + 'jcafb.bmp'
            image_file_path = template_dir_path + '/' + parameter.parameter
            # if not os.path.isfile(image_file_path):
            #     img = Image.open(template_dir_path + '/' + 'jcafb.png')
            #     r, g, b, a = img.split()
            #     img = Image.merge('RGB', (r, g, b))
            #     img.save(image_file_path)
            sheet.insert_bitmap(image_file_path, 0, 3)

        parameters = LabTestTypeExportXlsParam.search([
            ('lab_test_type_id', '=', lab_test_type_id),
            ('display', '=', 'result'),
            ('parameter_type', '=', 'variable_name'),
        ])

        for parameter in parameters:

            # ExportXLS.setOutCell(sheet, 11, 3, lab_test_request_code)
            # ExportXLS.setOutCell(sheet, 35, 3, lab_test_result_code)
            # ExportXLS.setOutCell(sheet, 11, 5, reference_name)
            # ExportXLS.setOutCell(sheet, 11, 7, reference_code)
            # ExportXLS.setOutCell(sheet, 11, 9, received_by_name)
            # ExportXLS.setOutCell(sheet, 11, 10, received_by_code)
            # ExportXLS.setOutCell(sheet, 11, 11, date_received)
            ExportXLS.setOutCell(sheet, parameter.col_nr, parameter.row_nr, eval(parameter.parameter))

        parameters = LabTestTypeExportXlsParam.search([
            ('lab_test_type_id', '=', lab_test_type_id),
            ('display', '=', 'result'),
            ('parameter_type', '=', 'expression'),
        ])

        for parameter in parameters:

            ExportXLS.setOutCell(sheet, parameter.col_nr, parameter.row_nr, eval(parameter.parameter))

        save_book = True

        if save_book:

            wbook.save(file_path)

            self.directory_id = file_system_directory.id
            self.file_name = file_name
            self.stored_file_name = file_name

        return True

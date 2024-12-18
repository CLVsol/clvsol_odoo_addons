# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import xlwt
from xlutils.copy import copy
from xlrd import open_workbook
from datetime import datetime

# from shutil import copyfile

# import os.path
# from PIL import Image

from odoo import models

_logger = logging.getLogger(__name__)


class LabTestResult(models.Model):
    _name = "clv.lab_test.result"
    _inherit = 'clv.lab_test.result'

    def lab_test_result_report_export_xls(self, dir_path, file_name, use_template, template_dir_path):

        lab_test_type = self.lab_test_type_id.code
        lab_test_result_code = self.code

        FileSystemDirectory = self.env['clv.file_system.directory']
        file_system_directory = FileSystemDirectory.search([
            ('directory', '=', dir_path),
        ])

        if use_template:
            template_file_name = self.lab_test_type_id.template_file_name_report
            template_file_path = template_dir_path + '/' + template_file_name
            book = open_workbook(template_file_path, formatting_info=True)
            wbook = copy(book)
            sheet = wbook.get_sheet(0)
            file_name = file_name.replace('<type>', lab_test_type).replace('<result_code>', lab_test_result_code)
            file_path = dir_path + '/' + file_name
            idx = book.sheet_names().index(template_file_name)
            wbook.get_sheet(idx).name = file_name
        else:
            file_name = file_name.replace('<type>', lab_test_type).replace('<result_code>', lab_test_result_code)
            file_path = dir_path + '/' + file_name
            wbook = xlwt.Workbook()
            sheet = wbook.add_sheet(file_name)

        lab_test_type_id = self.lab_test_type_id.id
        reference_name = self.ref_id.name
        reference_code = self.ref_id.code
        professional_name = self.employee_id.name
        professional_id = self.employee_id.professional_id
        date_approved = datetime.strftime(self.date_approved, '%d-%m-%Y')

        _logger.info(u'%s %s %s %s', '>>>>>>>>>>', lab_test_result_code, lab_test_type, use_template)

        save_book = False

        ExportXLS = self.env['clv.export_xls']

        LabTestTypeExportXlsParam = self.env['clv.lab_test.export_xls.param']

        parameters = LabTestTypeExportXlsParam.search([
            ('lab_test_type_id', '=', lab_test_type_id),
            ('display', '=', 'report'),
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
            ('display', '=', 'report'),
            ('parameter_type', '=', 'variable_name'),
        ])

        for parameter in parameters:

            # ExportXLS.setOutCell(sheet, 6, 7, reference_name)
            # ExportXLS.setOutCell(sheet, 35, 7, reference_code)
            # ExportXLS.setOutCell(sheet, 9, 9, date_approved)
            # ExportXLS.setOutCell(sheet, 38, 9, lab_test_result_code)
            # ExportXLS.setOutCell(sheet, 33, 57, professional_name)
            # ExportXLS.setOutCell(sheet, 36, 58, professional_id)
            ExportXLS.setOutCell(sheet, parameter.col_nr, parameter.row_nr, eval(parameter.parameter))

        parameters = LabTestTypeExportXlsParam.search([
            ('lab_test_type_id', '=', lab_test_type_id),
            ('display', '=', 'report'),
            ('parameter_type', '=', 'expression'),
        ])

        for parameter in parameters:

            ExportXLS.setOutCell(sheet, parameter.col_nr, parameter.row_nr, eval(parameter.parameter))

        parameters = LabTestTypeExportXlsParam.search([
            ('lab_test_type_id', '=', lab_test_type_id),
            ('display', '=', 'report'),
            ('parameter_type', '=', 'result_code'),
        ])

        for parameter in parameters:

            # result = self.criterion_ids.search([
            #     ('lab_test_result_id', '=', self.lab_test_result_id.id),
            #     ('code', '=', 'EAN21_03_02'),
            # ]).result
            # if result_peso is not False:
            #     ExportXLS.setOutCell(sheet, 16, 23, result)

            # result_peso = self.criterion_ids.search([
            #     ('lab_test_result_id', '=', self.lab_test_result_id.id),
            #     ('code', '=', 'EAN21_02_01'),
            # ]).result
            # if result_peso is not False:
            #     ExportXLS.setOutCell(sheet, 5, 29, result_peso)

            # result_altura = self.criterion_ids.search([
            #     ('lab_test_result_id', '=', self.lab_test_result_id.id),
            #     ('code', '=', 'EAN21_02_03'),
            # ]).result
            # if result_altura is not False:
            #     ExportXLS.setOutCell(sheet, 18, 29, result_altura)

            result = self.criterion_ids.search([
                ('lab_test_result_id', '=', self.id),
                ('code', '=', parameter.parameter),
            ]).result
            if result is not False:
                ExportXLS.setOutCell(sheet, parameter.col_nr, parameter.row_nr, result)

        save_book = True

        if save_book:

            wbook.save(file_path)

            self.directory_id_report = file_system_directory.id
            self.file_name_report = file_name
            self.stored_file_name_report = file_name

        return True

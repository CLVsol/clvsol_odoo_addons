# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import logging
from datetime import *
import xlwt

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ObjectModelExport(models.AbstractModel):
    _inherit = 'clv.object.model_export'

    def model_export_file_name(self, export_type):
        if export_type == 'xls':
            return '<model>_<label>_<code>_<timestamp>.xls'
        return False


class ModelExport(models.Model):
    _description = 'Model Export'
    _name = 'clv.model_export'
    _inherit = 'clv.object.model_export', 'clv.code.model'

    code = fields.Char(string='Model Export Code', required=False, default='/')
    code_sequence = fields.Char(default='clv.export.code')

    template_id = fields.Many2one(
        comodel_name='clv.model_export.template',
        string='Model Export Template',
        required=False,
        ondelete='restrict'
    )

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    @api.onchange('template_id')
    def onchange_template_id(self):

        if self.template_id:
            self.name = self.template_id.name
            self.label = self.template_id.label
            self.model_id = self.template_id.model_id
            self.export_type = self.template_id.export_type
            self.notes = self.template_id.notes

    @api.model
    def create(self, values):

        ModelExportField = self.env['clv.model_export.field']

        new_model_export = super(ModelExport, self).create(values)

        model_export_field_ids = []
        for model_export_template_field in new_model_export.template_id.model_export_template_field_ids:
            values = {
                'name': model_export_template_field.name,
                'model_export_id': new_model_export.id,
                'field_id': model_export_template_field.field_id.id,
                'sequence': model_export_template_field.sequence,
            }
            new_model_export_template_field = ModelExportField.create(values)
            model_export_field_ids += [new_model_export_template_field.id]

        return new_model_export

    @api.multi
    def write(self, values):

        ModelExportField = self.env['clv.model_export.field']

        res = super(ModelExport, self).write(values)

        if 'template_id' in values:

            for model_export_field in self.model_export_field_ids:
                model_export_field.unlink()

            model_export_field_ids = []
            for model_export_template_field in self.template_id.model_export_template_field_ids:
                values = {
                    'name': model_export_template_field.name,
                    'model_export_id': self.id,
                    'field_id': model_export_template_field.field_id.id,
                    'sequence': model_export_template_field.sequence,
                }
                new_model_export_template_field = ModelExportField.create(values)
                model_export_field_ids += [new_model_export_template_field.id]

        return res

    @api.multi
    def do_model_export_execute_xls(self, dir_path, file_name):

        from time import time
        start = time()

        FileSystemDirectory = self.env['clv.file_system.directory']
        file_system_directory = FileSystemDirectory.search([
            ('directory', '=', dir_path),
        ])

        self.date_export = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        model_name = self.model_id.name
        label = ''
        if self.label is not False:
            label = '_' + self.label
        code = self.code
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')[2:]
        file_name = file_name\
            .replace('<model>', model_name)\
            .replace('_<label>', label)\
            .replace('<code>', code)\
            .replace('<timestamp>', timestamp)
        file_path = dir_path + '/' + file_name
        _logger.info(u'%s %s', '>>>>>>>>>>', file_path)

        book = xlwt.Workbook()

        sheet = book.add_sheet(file_name)
        row_nr = 0

        row = sheet.row(row_nr)
        col_nr = 0
        for field in self.model_export_field_ids:
            col_name = field.field_id.field_description
            if field.name is not False:
                col_name = field.name
            row.write(col_nr, col_name)
            col_nr += 1

        item_count = 0
        items = False
        if (self.export_all_items is False) and \
           (self.model_items is not False):
            items = eval('self.' + self.model_items)
        elif self.export_all_items is True:
            Model = self.env[self.model_model]
            items = Model.search(eval(self.export_domain_filter))

        if items is not False:
            for item in items:
                item_count += 1
                row_nr += 1
                row = sheet.row(row_nr)
                col_nr = 0
                for field in self.model_export_field_ids:
                    if field.field_id.ttype == 'date':
                        cmd = 'item.' + field.field_id.name
                        if eval(cmd) is not False:
                            date_value = eval(cmd)
                        date_obj = datetime.strptime(date_value, DEFAULT_SERVER_DATE_FORMAT)
                        try:
                            date_formated = datetime.strftime(date_obj, self.date_format)
                        except Exception:
                            date_formated = date_value
                        cmd = '"' + date_formated + '"'
                    elif field.field_id.ttype == 'datetime':
                        cmd = 'item.' + field.field_id.name
                        if eval(cmd) is not False:
                            datetime_value = eval(cmd)
                        datetime_obj = datetime.strptime(datetime_value, DEFAULT_SERVER_DATETIME_FORMAT)
                        try:
                            datetime_formated = datetime.strftime(datetime_obj, self.datetime_format)
                        except Exception:
                            datetime_formated = datetime_value
                        cmd = '"' + datetime_formated + '"'
                    elif field.field_id.ttype == 'many2many':
                        cmd = 'item.' + field.field_id.name + '.name'
                    elif field.field_id.ttype == 'many2one':
                        cmd = 'item.' + field.field_id.name + '.name'
                    else:
                        cmd = 'item.' + field.field_id.name
                    if eval(cmd) is not False:
                        row.write(col_nr, eval(cmd))
                    col_nr += 1

                _logger.info(u'>>>>>>>>>>>>>>> %s %s', item_count, item.code)

        book.save(file_path)

        self.directory_id = file_system_directory.id
        self.file_name = file_name
        self.stored_file_name = file_name

        _logger.info(u'%s %s', '>>>>>>>>>> file_path: ', file_path)
        _logger.info(u'%s %s', '>>>>>>>>>> item_count: ', item_count)
        _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))


class ModelExportTemplate(models.Model):
    _inherit = 'clv.model_export.template'

    model_export_ids = fields.One2many(
        comodel_name='clv.model_export',
        inverse_name='template_id',
        string='Model Exports'
    )
    count_model_exports = fields.Integer(
        string='Model Exports',
        compute='_compute_count_model_exports',
        store=True
    )

    @api.multi
    @api.depends('model_export_ids')
    def _compute_count_model_exports(self):
        for r in self:
            r.count_model_exports = len(r.model_export_ids)

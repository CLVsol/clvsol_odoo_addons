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

from odoo import models


class ExportXLS(models.AbstractModel):
    _description = 'Export XLS'
    _name = 'clv.export_xls'

    '''
    Reference:
        Preserving styles using python's xlrd, xlwt, and xlutils.copy
        https://stackoverflow.com/questions/3723793/preserving-styles-using-pythons-xlrd-xlwt-and-xlutils-copy

        There are two parts to this.
        First, you must enable the reading of formatting info when opening the source workbook.
        The copy operation will then copy the formatting over.

            import xlrd
            import xlutils.copy

            inBook = xlrd.open_workbook('input.xls', formatting_info=True)
            outBook = xlutils.copy.copy(inBook)

        Secondly, you must deal with the fact that changing a cell value resets the formatting of that cell.
        This is less pretty; I use the following hack where I manually copy the formatting index (xf_idx) over:
    '''

    def _getOutCell(self, outSheet, colIndex, rowIndex):
        """ HACK: Extract the internal xlwt cell representation. """
        row = outSheet._Worksheet__rows.get(rowIndex)
        if not row:
            return None

        cell = row._Row__cells.get(colIndex)
        return cell

    def setOutCell(self, outSheet, col, row, value):
        """ Change cell value without changing formatting. """
        # HACK to retain cell style.
        previousCell = self._getOutCell(outSheet, col, row)
        # END HACK, PART I

        outSheet.write(row, col, value)

        # HACK, PART II
        if previousCell:
            newCell = self._getOutCell(outSheet, col, row)
            if newCell:
                newCell.xf_idx = previousCell.xf_idx
        # END HACK

    '''
    outSheet = outBook.get_sheet(0)
    setOutCell(outSheet, 5, 5, 'Test')
    outBook.save('output.xls')
    '''

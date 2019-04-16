# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ModelExport_xls(models.Model):
    _inherit = 'clv.model_export'

    @api.multi
    def do_model_export_execute_xls_person(self):

        self.do_model_export_execute_xls()


class ModelExport_csv(models.Model):
    _inherit = 'clv.model_export'

    @api.multi
    def do_model_export_execute_csv_person(self):

        self.do_model_export_execute_csv()


class ModelExport_sqlite(models.Model):
    _inherit = 'clv.model_export'

    @api.multi
    def do_model_export_execute_sqlite_person(self):

        self.do_model_export_execute_sqlite()

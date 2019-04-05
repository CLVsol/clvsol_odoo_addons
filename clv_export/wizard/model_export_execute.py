# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ModelExportSetUp(models.TransientModel):
    _description = 'Model Export SetUp'
    _name = 'clv.model_export.execute'

    def _default_model_export_ids(self):
        return self._context.get('active_ids')
    model_export_ids = fields.Many2many(
        comodel_name='clv.model_export',
        relation='clv_model_export_execute_rel',
        string='Model Exports',
        default=_default_model_export_ids)

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_model_export_execute(self):
        self.ensure_one()

        for model_export in self.model_export_ids:

            _logger.info(u'%s %s', '>>>>>', model_export.name)

            if model_export.export_type == 'xls':
                model_export.do_model_export_execute_xls()

            if model_export.export_type == 'sqlite':
                model_export.do_model_export_execute_sqlite()

        return True

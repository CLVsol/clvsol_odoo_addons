# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
# from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PartnerStreetPatterntSearch(models.TransientModel):
    _description = 'Partner Street Pattern Search'
    _name = 'res.partner.street_pattern.search'

    def _default_res_partner_ids(self):
        return self._context.get('active_ids')
    res_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='res_partner_street_pattern_search_rel',
        string='Partners',
        readonly=True,
        default=_default_res_partner_ids
    )

    # def _default_employee_id(self):
    #     HrEmployee = self.env['hr.employee']
    #     employee = HrEmployee.search([
    #         ('user_id', '=', self.env.uid),
    #     ])
    #     if employee.id is not False:
    #         return employee.id
    #     return False
    # employee_id = fields.Many2one(
    #     comodel_name='hr.employee',
    #     string='Searchd by',
    #     required=True,
    #     default=_default_employee_id
    # )

    # date_searchd = fields.Datetime(
    #     string='Searchd Date',
    #     required=True,
    #     default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # )

    def do_res_partner_street_pattern_search(self):
        self.ensure_one()

        # current_phase_id = int(self.env['ir.config_parameter'].sudo().get_param(
        #     'clv.global_settings.current_phase_id', '').strip())

        # for res_partner in self.res_partner_ids:

        #     _logger.info(u'%s %s %s', '>>>>>', res_partner.phase_id.id, res_partner.ref_name)

        #     if (res_partner.phase_id.id == current_phase_id) and \
        #        (res_partner.state == 'new'):

        #         _logger.info(u'%s %s %s', '>>>>>', self.employee_id.name, self.date_searchd)

        #         res_partner.employee_id_request = self.employee_id
        #         res_partner.date_searchd = self.date_searchd
        #         res_partner.state = 'searchd'
        #         res_partner.reg_state = 'revised'

        return True

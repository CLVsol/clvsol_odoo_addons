# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabTestRequest(models.Model):
    _inherit = 'clv.lab_test.request'

    state = fields.Selection(
        [('draft', 'Draft'),
         ('received', 'Received'),
         ('cancelled', 'Cancelled'),
         ], 'Request State', readonly=True
    )

    def action_draft(self):
        pass

    def action_received(self):
        pass

    def action_cancel(self):
        pass

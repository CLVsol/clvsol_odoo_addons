# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class FamilyOff(models.Model):
    _inherit = 'clv.family_off'

    off_instance_id = fields.Many2one(
        comodel_name='clv.off.instance',
        string='Off Instance',
        required=False,
    )

# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class DataProcessingBatchMember(models.Model):
    _name = "clv.data_processing.batch.member"
    _inherit = 'clv.data_processing.batch.member', 'clv.abstract.reference'

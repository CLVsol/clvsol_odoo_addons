# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProcessingHost(models.Model):
    _description = 'Processing Host'
    _name = 'clv.processing.host'
    _order = 'name'

    name = fields.Char(
        string='External Host Name',
        required=True,
        help='Processing Host Name (Example: http://localhost:8069'
    )

    external_dbname = fields.Char(
        string='External Database Name',
        help='External Database Name'
    )
    external_user = fields.Char(
        string='External User',
        help='Processing User'
    )
    external_user_pw = fields.Char(
        string='External User Password',
        help='Processing User Password'
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
    ]

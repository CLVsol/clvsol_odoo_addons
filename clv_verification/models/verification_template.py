# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VerificationTemplate(models.Model):
    _description = 'Verification Template'
    _name = 'clv.verification.template'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        help='Verification Template Name'
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    model = fields.Char(
        string='Model',
        required=True,
        help="Model name of the object on which the verification method to be called is located, e.g. 'res.partner'"
    )

    method = fields.Char(
        string='Method',
        required=False,
        help="Name of the method to be called when the verification job is processed."
    )

    method_args = fields.Text(
        string='Method Arguments',
        required=False,
        help="List  of arguments(Python dictionary format) for the method.",
        default='{}'
    )

    action = fields.Char(
        string='Action',
        required=False,
        help="Name of the action used to process the verification."
    )

    action_args = fields.Text(
        string='Action Arguments',
        required=False,
        help="List  of arguments(Python dictionary format) for the action.",
        default='{}'
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Name must be unique!'),
    ]

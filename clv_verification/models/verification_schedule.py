# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class VerificationSchedule(models.Model):
    _description = 'Verification Schedule'
    _name = 'clv.verification.schedule'
    _order = 'name'

    template_id = fields.Many2one(
        comodel_name='clv.verification.template',
        string='Verification Template',
        required=False,
        ondelete='restrict'
    )

    name = fields.Char(
        string='Name',
        required=True,
        help='Verification Schedule Name'
    )

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string='Inclusion Date',
        default=fields.Datetime.now)

    date_last_verification = fields.Datetime(
        string='Last Verification Date',
        readonly=True
    )

    model = fields.Char(
        string='Model',
        required=False,
        help="Model name of the object on which the verification action to be called is located, e.g. 'res.partner'"
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

    model_items = fields.Char(
        string='Model Items',
        compute='compute_model_items',
        store=False
    )

    verify_all_items = fields.Boolean(string='Verify All Items', default=True)

    verification_domain_filter = fields.Text(
        string='Verification Domain Filter',
        required=False,
        help="Verification Domain Filter",
        default='[]'
    )

    verification_log = fields.Text(
        string="Verification Log"
    )

    active = fields.Boolean(string='Active', default=1)

    date_last_verification = fields.Datetime(
        string='Last Verification Date',
        readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):

        schedule = super().create(vals_list)

        if schedule.template_id.id is not False:

            schedule.model = schedule.template_id.model
            schedule.method = schedule.template_id.method
            schedule.method_args = schedule.template_id.method_args
            schedule.action = schedule.template_id.action
            schedule.action_args = schedule.template_id.action_args

        return schedule

    @api.onchange('template_id')
    def onchange_template_id(self):
        if self.template_id.id:

            self.model = self.template_id.model
            self.method = self.template_id.method
            self.method_args = self.template_id.method_args
            self.action = self.template_id.action
            self.action_args = self.template_id.action_args

    @api.depends('model')
    def compute_model_items(self):
        for r in self:
            r.model_items = False


class VerificationTemplate(models.Model):
    _inherit = 'clv.verification.template'

    schedule_ids = fields.One2many(
        comodel_name='clv.verification.schedule',
        inverse_name='template_id',
        string='Schedules'
    )
    count_schedules = fields.Integer(
        string='Number of Schedules',
        compute='_compute_count_schedules',
        store=True
    )

    @api.depends('schedule_ids')
    def _compute_count_schedules(self):
        for r in self:
            r.count_schedules = len(r.schedule_ids)

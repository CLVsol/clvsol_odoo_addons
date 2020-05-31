# -*- coding: utf-8 -*-
# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2016 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    type = fields.Selection(selection_add=[
        ('clv.patient', 'Patient'),
    ])
    # alias = fields.Char(
    #     string='Alias',
    #     help='Common name that the Partner is referred',
    # )
    patient_ids = fields.One2many(
        string='Related Patients',
        comodel_name='clv.patient',
        compute='_compute_patient_ids_and_count',
    )
    count_patients = fields.Integer(
        compute='_compute_patient_ids_and_count',
    )
    # birthdate_date = fields.Date(
    #     string='Birthdate',
    # )
    # gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('other', 'Other'),
    # ])
    # weight = fields.Float()
    # weight_uom = fields.Many2one(
    #     string="Weight UoM",
    #     comodel_name="product.uom",
    #     default=lambda s: s.env['res.lang'].default_uom_by_category('Weight'),
    #     domain=lambda self: [('category_id', '=',
    #                           self.env.ref('product.product_uom_categ_kgm').id)
    #                          ]
    # )

    # @api.multi
    def _get_clv_entity(self):
        self.ensure_one()
        if self.type and self.type[:3] == 'clv':
            return self.env[self.type].search([
                ('partner_id', '=', self.id),
            ])

    # @api.multi
    def _compute_patient_ids_and_count(self):
        for record in self:
            patients = self.env['clv.patient'].search([
                ('partner_id', 'child_of', record.id),
            ])
            record.count_patients = len(patients)
            record.patient_ids = [(6, 0, patients.ids)]

    # @api.multi
    # @api.constrains('birthdate_date')
    # def _check_birthdate_date(self):
    #     """ It will not allow birthdates in the future. """
    #     now = datetime.now()
    #     for record in self:
    #         if not record.birthdate_date:
    #             continue
    #         birthdate = fields.Datetime.from_string(record.birthdate_date)
    #         if birthdate > now:
    #             raise ValidationError(_(
    #                 'Partners cannot be born in the future.',
    #             ))

    @api.model
    def create(self, vals):
        """ It overrides create to bind appropriate clv entity. """
        if all((
            vals.get('type', '').startswith('clv.'),
            not self.env.context.get('clv_entity_no_create'),
        )):
            model = self.env[vals['type']].with_context(
                clv_entity_no_create=True,
            )
            clv_entity = model.create(vals)
            return clv_entity.partner_id
        return super().create(vals)

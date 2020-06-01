# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AbstractHierarchicalCategory(models.AbstractModel):
    _description = 'Abstract Hierarchical Category'
    _name = 'clv.abstract.h_category'
    _parent_store = True
    _parent_order = 'name'
    # _order = 'parent_left'
    _order = 'name, parent_id'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', required=False)
    description = fields.Char(string='Description')
    notes = fields.Text(string='Notes')

    parent_id = fields.Many2one(
        comodel_name='clv.abstract.h_category',
        string='Parent Category',
        index=True,
        ondelete='restrict'
    )
    child_ids = fields.One2many(
        comodel_name='clv.abstract.h_category',
        inverse_name='parent_id',
        string='Child Categories'
    )

    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)
    parent_path = fields.Char(index=True)
    complete_name = fields.Char(
        string='Full Name',
        compute='_name_get_fnc',
        store=False,
        readonly=True
    )

    active = fields.Boolean(string='Active', default=True)

    color = fields.Integer(string='Color Index')

    # _constraints = [
    #     (models.Model._check_recursion,
    #      'Error! You can not create recursive categories.',
    #      ['parent_id']),
    # ]

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive categories.'))
        return True

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         'Error! The Code must be unique!'),
        ('name_uniq',
         'UNIQUE (parent_id, name)',
         'Error! The Name must be unique for the same Parent!'),
    ]

    # @api.multi
    def name_get(self):
        """Return the h_category's display name, including their direct parent by default.

        :param dict context: the ``h_category_display`` key can be
                             used to select the short version of the
                             h_category (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('h_category_display') == 'short':
            return super().name_get()

        res = []
        for record in self:
            names = []
            current = record
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((record.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        categories = self.search(args, limit=limit)
        return categories.name_get()

    # @api.one
    def _name_get_fnc(self):
        self.ensure_one()

        for record in self:
            record.refresh_complete_name = 0
            complete_name = record.name_get()
            if complete_name:
                record.complete_name = complete_name[0][1]
            else:
                record.complete_name = record.name

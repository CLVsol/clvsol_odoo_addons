# © 2016 Serpent Consulting Services Pvt. Ltd. (support@serpentcs.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class MediaFileFormatModel(models.AbstractModel):
    _name = 'clv.mfile.format.model'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    name = fields.Char(string='Format Name', required=True, translate=True)
    description = fields.Char(string='Description')
    notes = fields.Text(string='Notes')

    parent_left = fields.Integer(string='Left parent', index=True)
    parent_right = fields.Integer(string='Right parent', index=True)
    complete_name = fields.Char(
        string='Full Format Name',
        compute='_name_get_fnc',
        store=False,
        readonly=True
    )

    active = fields.Boolean(string='Active', default=True)

    color = fields.Integer(string='Color Index')

    _constraints = [
        (models.Model._check_recursion,
         'Error! You can not create recursive formats.',
         ['parent_id']),
    ]

    @api.multi
    def name_get(self):
        """Return the format's display name, including their direct parent by default.

        :param dict context: the ``format_display`` key can be
                             used to select the short version of the
                             format (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if self._context is None:
            self._context = {}
        if self._context.get('format_display') == 'short':
            return super(MediaFileFormatModel, self).name_get()
        if isinstance(self._ids, (int, long)):
            self._ids = [self._ids]
        reads = self.read(['name', 'parent_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        formats = self.search(args, limit=limit)
        return formats.name_get()

    @api.one
    def _name_get_fnc(self):
        self.refresh_complete_name = 0
        complete_name = self.name_get()
        if complete_name:
            self.complete_name = complete_name[0][1]
        else:
            self.complete_name = self.name


class MediaFileFormat(models.Model):
    _description = 'Media File Format'
    _name = 'clv.mfile.format'
    _inherit = 'clv.mfile.format.model'

    code = fields.Char(string='Format Code', required=False)

    parent_id = fields.Many2one(
        comodel_name='clv.mfile.format',
        string='Parent Format',
        index=True,
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='clv.mfile.format',
        inverse_name='parent_id',
        string='Child Formats'
    )

    mfile_ids = fields.Many2many(
        comodel_name='clv.mfile',
        relation='clv_mfile_format_rel',
        column1='format_id',
        column2='mfile_id',
        string='Media Files'
    )

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]


class MediaFile(models.Model):
    _inherit = "clv.mfile"

    format_ids = fields.Many2many(
        comodel_name='clv.mfile.format',
        relation='clv_mfile_format_rel',
        column1='mfile_id',
        column2='format_id',
        string='Formats'
    )
    format_names = fields.Char(
        string='Format Names',
        compute='_compute_format_names',
        store=True
    )
    format_names_suport = fields.Char(
        string='Format Names Suport',
        compute='_compute_format_names_suport',
        store=False
    )

    @api.depends('format_ids')
    def _compute_format_names(self):
        for r in self:
            r.format_names = r.format_names_suport

    @api.multi
    def _compute_format_names_suport(self):
        for r in self:
            format_names = False
            for format in r.format_ids:
                if format_names is False:
                    format_names = format.complete_name
                else:
                    format_names = format_names + ', ' + format.complete_name
            r.format_names_suport = format_names
            if r.format_names != format_names:
                record = self.env['clv.mfile'].search([('id', '=', r.id)])
                record.write({'format_ids': r.format_ids})

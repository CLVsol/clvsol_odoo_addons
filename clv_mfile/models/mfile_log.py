# © 2016 Serpent Consulting Services Pvt. Ltd. (support@serpentcs.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MediaFileLog(models.Model):
    _description = 'Media File Log'
    _name = 'clv.mfile.log'
    _inherit = 'clv.object.log'

    mfile_id = fields.Many2one(
        comodel_name='clv.mfile',
        string='MediaFile',
        required=True,
        ondelete='cascade'
    )


class MediaFile(models.Model):
    _name = "clv.mfile"
    _inherit = 'clv.mfile', 'clv.log.model'

    log_ids = fields.One2many(
        comodel_name='clv.mfile.log',
        inverse_name='mfile_id',
        string='Media File Log',
        readonly=True
    )

    @api.one
    def insert_object_log(self, mfile_id, values, action, notes):
        if self.active_log or 'active_log' in values:
            vals = {
                'mfile_id': mfile_id,
                'values': values,
                'action': action,
                'notes': notes,
            }
            self.env['clv.mfile.log'].create(vals)

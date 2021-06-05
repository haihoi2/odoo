from odoo import models, fields, api


class Project(models.Model):
    _inherit = "project.project"

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.uid,
                                   compute='_get_current_user')

    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user.id

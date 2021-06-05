from odoo import models, fields, api


class AccountAnalyticLineCustom(models.Model):
    _inherit = 'account.analytic.line'

    name = fields.Char('Note From Engineer', required=False)
    evaluation_from_assigner = fields.Char('Evaluation From Assigner', required=False)

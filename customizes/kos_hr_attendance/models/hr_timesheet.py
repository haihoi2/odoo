from odoo import models, fields, api


class HrTimesheet(models.Model):
    _inherit = "account.analytic.line"

    note_from_assigner = fields.Char("Note From Assigner", required=False)

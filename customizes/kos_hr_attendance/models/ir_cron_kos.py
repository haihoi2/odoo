from odoo import models, fields, api


class IrCronKos(models.Model):
    _inherit = 'ir.actions.server'

    code = fields.Text(string='Python Code', groups='base.group_system, base.group_erp_manager, kos_hr_attendance.Schedule',
                       help="Write Python code that the action will execute. Some variables are "
                            "available for use; help about python expression is given in the help tab.")

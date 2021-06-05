from odoo import models, fields, api


class AccountAnalyticLineCustom(models.Model):
    _name = "account.analytic.line"
    _inherit = ['account.analytic.line', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Note From Engineer', required=False, track_visibility='onchange')
    evaluation_from_assigner = fields.Char('Evaluation From Assigner', required=False, track_visibility='onchange',
                                           readonly=True)
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today,
                       track_visibility='onchange')
    amount = fields.Monetary('Amount', required=True, default=0.0, track_visibility='onchange')
    task_id = fields.Many2one('project.task', 'Task', index=True, domain="[('company_id', '=', company_id)]",
                              track_visibility='onchange')
    project_id = fields.Many2one('project.project', 'Project', domain=[('allow_timesheets', '=', True)],
                                 track_visibility='onchange')
    unit_amount = fields.Float('Quantity', default=0.0, track_visibility='onchange')
    tag_ids = fields.Many2many('account.analytic.tag', 'account_analytic_line_tag_rel_2', 'line_id_2', 'tag_id',
                               string='Tags', copy=True,
                               domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
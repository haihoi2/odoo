# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.http import request


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    def _attendance_action_change(self):
        ha_obj = super(HrEmployeeBase, self)._attendance_action_change()
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        if self.attendance_state != 'checked_out':
            checkin_status = self.env.context.get("checkin_status", False)
            ha_obj.update({'checkin_status': checkin_status})
            ha_obj.update({'ip_address': ip_address})
            reason_late = self.env.context.get("reason_late", False)
            if reason_late:
                ha_obj.update({'reason_late': reason_late})
        elif self.attendance_state == 'checked_out':
            checkout_status = self.env.context.get("checkout_status", False)
            ha_obj.update({'ip_address_out': ip_address})
            ha_obj.update({'checkout_status': checkout_status})
        return ha_obj

    def attendance_manual(self, next_action, entered_pin=None, reason_late='', checkin_status='', checkout_status=''):
        next_action = 'hr_attendance.hr_attendance_action'
        res = super(
            HrEmployeeBase, self.with_context(reason_late=reason_late, checkin_status=checkin_status,
                                              checkout_status=checkout_status)
        ).attendance_manual(next_action, entered_pin)
        return res


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    code = fields.Char("Code", size=10, required=True)

    _sql_constraints = [
        ('code_company_uniq', 'unique (code,company_id)',
         'The code of the employee must be unique per company !')
    ]


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    code = fields.Char("Code", size=10, required=True)

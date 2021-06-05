# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError
import pytz


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    ip_address = fields.Char(string="Check-in IP", readonly=True)
    ip_address_out = fields.Char(string="Check-out IP", readonly=True)
    reason_late = fields.Char('Reason late')
    checkin_status = fields.Char(string="Checkin Status", default="None")
    checkout_status = fields.Char(string="Checkout Status", default="None")
    employee_id = fields.Many2one('hr.employee', store=True)
    manager_id = fields.Many2one(related='employee_id.parent_id', store=True)
    location_in = fields.Char(compute="get_location_by_ip_in", default="None")
    location_out = fields.Char(compute="get_location_by_ip_out", default="None")

    @api.model
    def get_location_by_ip_in(self):
        attendances = self.env['hr.attendance'].search([])
        for attendance in attendances:
            location = self.env['hr.location'].search([('ip_address', '=', attendance.ip_address)], limit=1)
            if location:
                attendance.location_in = location.location
            else:
                attendance.location_in = "-"

    @api.model
    def get_location_by_ip_out(self):
        attendances = self.env['hr.attendance'].search([])
        for attendance in attendances:
            location = self.env['hr.location'].search([('ip_address', '=', attendance.ip_address_out)], limit=1)
            if location:
                attendance.location_out = location.location
            else:
                attendance.location_out = "-"

    def auto_checkout_after_dailytime(self, hour, minute, second, microsecond):
        now = datetime.now()
        today_at_dailytime = datetime.now().replace(hour=hour - 7, minute=minute, second=second,
                                                    microsecond=microsecond)
        attendances = self.env['hr.attendance'].search([])
        if now > today_at_dailytime:
            for attendance in attendances:
                if not attendance.check_out:
                    attendance.checkout_status = "Missing data"
                    attendance.check_out = fields.Datetime.now()
                    attendance.ip_address_out = '0.0.0.0'
        # timezone_vn = pytz.timezone('Asia/Ho_Chi_Minh')
        # now = datetime.now(timezone_vn)
        # today_at_23h59 = datetime.now(timezone_vn).replace(hour=hour - 7, minute=minute, second=second,
        #                                                   microsecond=microsecond)
        # today_at_23h59 = fields.Datetime.now().replace(hour=hour - 7, minute=minute, second=second,
        #                                                microsecond=microsecond)

    # prevent user create record for another
    @api.model
    def create(self, values):
        if 'employee_id' in values:
            employee = self.env['hr.employee'].browse(
                values.get('employee_id'))
            current_employee = self.env['hr.employee'].search(
                [('user_id', '=', self.env.user.id)])
            if employee != current_employee:
                raise UserError(
                    'You are not allowed to create record for another')
        return super(HrAttendance, self).create(values)

    # prevent user to pick a future day in check_in and check_out field
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        from lxml import etree

        res = super(HrAttendance, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='check_in' or @name='check_out']"):
                node.set('options', "{'datepicker': {'maxDate': '%sT23:59:59'}}" % fields.Date.today(
                ).strftime(DEFAULT_SERVER_DATE_FORMAT))
            res['arch'] = etree.tostring(doc)
        return res

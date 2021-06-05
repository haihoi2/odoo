from odoo import models, fields, api


class LocationByIp(models.Model):
    _name = "hr.location"

    ip_address = fields.Char()
    location = fields.Char(string="Location", default="-")
    note_text = fields.Char(string='Note')

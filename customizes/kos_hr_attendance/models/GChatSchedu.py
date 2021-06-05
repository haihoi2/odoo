from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
import requests
import json




class GChatSchedule(models.Model):
    _name = 'gchat.schedule'
    # _description = 'Schedule GChat'

    def auto_send_mess_Gchat(self, mess, _url):

        message = mess
        url = _url

        payload = json.dumps({
            "text": message
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)

        # server = '192.168.50.117'
        # database = 'kyanonOdoo13'
        # username = 'odoo'
        # password = 'Ky@n0n123'
        # cnxn = pyodbc.connect(SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        # cursor = cnxn.cursor()
        #
        # sql1 = f"SELECT mess FROM ir.cron WHERE cron_name = '{gchat}'"
        # e1 = cursor.execute(sql1)
        # data = e1.fetchall()
        # print(data)

        # SQL = ("SELECT mess FROM ir.cron WHERE cron_name = gchat")
        # self.env.cr.execute(SQL)
        # for row in self.env.cr.fetchall():
        #     return row
        #
        # print(row)





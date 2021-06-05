# -- coding: utf-8 --
import json
import requests

from odoo import api, fields, models
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import AccessDenied, UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    def _default_home_action(self):
        return self.env.ref('hr_attendance.hr_attendance_action_my_attendances').id or False

    action_id = fields.Many2one('ir.actions.actions', string='Home Action',
                                help="If specified, this action will be opened at log on for this user, in addition to the standard menu.",
                                default=_default_home_action)

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        """ retrieve and sign in the user corresponding to provider and validated access token
            :param provider: oauth provider id (int)
            :param validation: result of validation of access token (dict)
            :param params: oauth parameters (dict)
            :return: user login (str)
            :raise: AccessDenied if signin failed

            This method can be overridden to add alternative signin methods.
        """
        oauth_uid = validation['user_id']
        try:
            oauth_user = self.search(
                [("oauth_uid", "=", oauth_uid), ('oauth_provider_id', '=', provider)])
            if not oauth_user:
                # Check Staff Users
                oauth_user = self.search(
                    [("login", "=", validation['email']), ('oauth_provider_id', '=', provider)])
                if not oauth_user:
                    email = validation['email']
                    arr = email.split('@')
                    email_name = arr[0]
                    domain_tail = arr[1]
                    if domain_tail == "kyanon.digital":
                        vals_user = {
                            'name': email_name,
                            'login': email,
                            'email': email,
                            'oauth_provider_id': 3,
                            'oauth_access_token': params['access_token'],
                        }
                        self.env['res.users'].create(vals_user)

                        oauth_user = self.search(
                            [("login", "=", email), ('oauth_provider_id', '=', 3),
                             ('oauth_access_token', '=', params['access_token'])])
                        vals_employee = {
                            'name': arr[0],
                            'work_email': email,
                            'user_id': oauth_user.id,
                        }
                        self.env['hr.employee'].create(vals_employee)
                    else:
                        print("You are not Kyanon's company. You can not login.")
                    # raise AccessDenied()
                assert len(oauth_user) == 1
                oauth_user.write(
                    {'oauth_uid': oauth_uid, 'oauth_access_token': params['access_token']})
                return oauth_user.login
            assert len(oauth_user) == 1
            oauth_user.write({'oauth_access_token': params['access_token']})
            return oauth_user.login
        except AccessDenied as access_denied_exception:
            if self.env.context.get('no_user_creation'):
                return None
            state = json.loads(params['state'])
            token = state.get('t')
            values = self._generate_signup_values(provider, validation, params)
            try:
                _, login, _ = self.signup(values, token)
                return login
            except (SignupError, UserError):
                raise access_denied_exception

    def _is_cheked_in(self):
        self.ensure_one()
        if not self._is_public() and self.employee_id and self.employee_id.attendance_state == 'checked_in':
            return True
        return False
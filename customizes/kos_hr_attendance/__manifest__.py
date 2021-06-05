# -*- coding: utf-8 -*-
{
    'name': 'KOS Attendances',
    'version': '1.0',
    'category': 'Human Resources/Attendances',
    'sequence': 85,
    'summary': 'Kyanon Digital System Track employee attendance',
    'description': """
This module aims to manage employee's attendances.
==================================================
       """,
    'depends': ['hr', 'hr_attendance', 'base', 'web', 'auth_oauth', 'website', 'analytic', 'project', 'mail'],
    'data': [
        'security/hr_attendance_security.xml',
        'security/ir.model.access.csv',
        'views/hr_attendance_view.xml',
        'views/hr_employee_view.xml',
        'views/webclient_template.xml',
        'views/auth_oauth_templates.xml',
        'views/portal_templates.xml',
        "views/assets.xml",
        "views/logoCompany.xml",
        "views/hidden_all_features.xml",
        "views/filter_by_managername.xml",
        "views/auto_checkout_after_dailytime.xml",
        "views/location_by_ip.xml",
        "security/create_groups.xml",
        # "views/note_from_assigner.xml",
        # "views/account_analytic_line_inherit.xml",
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
    'application': True,
}

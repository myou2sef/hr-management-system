# -*- coding: utf-8 -*-
{
    'name': 'HR Attendance Report',
    'version': '17.0.1.0.0',
    'summary': 'Generate detailed attendance reports',
    'description': """
        HR Attendance Report Module
        =========================
        * Generate attendance reports by employee or department
        * Export reports in PDF or Excel format
        * View daily, weekly, and monthly attendance summaries
        * Access reports directly from employee profile
        * Quick access from attendance views
    """,
    'category': 'Human Resources/Employees',
    'author': 'Aspire Solutions',
    'website': 'https://www.aspiresoftware.in',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'hr',
        'hr_attendance',
        'to_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_report_views.xml',
        'wizard/attendance_report_wizard.xml',
    ],
    'images': ['static/description/banner.png'],
    'application': True,
    'installable': True,
}

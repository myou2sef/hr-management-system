# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'HR Attendance Report (Community)',
    'version': '14.0.1.0.0',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'HR',
    'description': """
        Module allows to Print report from Hr Attendance.
    """,
    'website': 'http://www.acespritech.com',
    'price': 30,
    'currency': 'EUR',
    'summary': 'Module allows to print report from Hr Attendance.',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/attendance_report_wizard.xml',
        'report/attendance_report_pdf.xml',
        'report/attendance_reports.xml',

    ],
    'images': ['static/description/4_pdf_report_department.png'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-
{
    'name': "Base Module",
    'version': '17.0.1.0.0',
    'summary': """Basic utilities and tools""",
    'description': """Base module that provides additional tools and utilities for HR Attendance""",
    'category': 'Human Resources/Attendance',
    'author': 'Aspire Solutions',
    'company': 'Aspire Solutions',
    'website': "https://www.aspiresoftware.in",
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/to_base_views.xml',
        'wizard/base_export_language_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'sequence': 0,
}

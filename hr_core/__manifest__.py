{
    'name': 'HR Core',
    'version': '1.0',
    'category': 'Human Resources',
    'sequence': 1,
    'summary': 'Core HR Management System',
    'description': """
        Core module for HR Management System
        ==================================
        This module provides the core functionality for HR management including:
        * Employee Management
        * Department & Position Management
        * Document Management
        * Organization Structure
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base'],
    'data': [
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_department_views.xml',
        'views/hr_position_views.xml',
        'views/hr_menu_views.xml',
        'data/hr_data.xml',
    ],
    'demo': [
        'demo/hr_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'hr_core/static/src/css/hr_styles.css',
            'hr_core/static/src/js/hr_core.js',
        ],
        'web.assets_qweb': [
            'hr_core/static/src/xml/hr_templates.xml',
        ],
    },
    'license': 'LGPL-3',
}

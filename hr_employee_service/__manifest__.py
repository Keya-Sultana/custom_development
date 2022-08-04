{
    'name': 'HR Employee Service',
    'version': "15.0.1.0.0",
    'category': 'Human Resources',
    'website': 'www.odoo.com.bd',
    'author': 'Odoo Bangladesh, ',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'summary': 'Employee service information & duration',
    'depends': [
        'hr',
    ],
    'external_dependencies': {
        'python': [
            'dateutil',
        ],
    },
    'data': [
        'views/hr_employee.xml',
    ],
    'license': 'LGPL-3',
}



{
    'name' : 'YUKO Holiday Allowance',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'HR',
    'description': """
    
    """,
    'category': 'Human Resources',
    'sequence': 4,
    'website' : '',
    'depends' : ['gbs_hr_security', 'hr',
                 'hr_holiday_allowance'],

    'data' : [
            'views/holiday_allowance_view.xml',
            ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

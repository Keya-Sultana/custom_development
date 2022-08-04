
{
    'name' : 'Yuko Sales',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Sales',
    'description': """
    
    """,
    'category': '',
    'sequence': 4,
    'website' : '',
    'depends' : ["sale",
                 'sales_team',
                 'purchase',
                 'yuko_report_layout',
                 ],
    'data' : ['security/security.xml',
              'security/ir.model.access.csv',
              'views/sale_order_views.xml',
              'reports/inherit_sale_report_templates.xml',],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

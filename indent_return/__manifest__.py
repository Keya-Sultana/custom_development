{
    'name' : 'Indent Return',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'description': """
    
    """,
    'category': 'Warehouse Management',
    'sequence': 4,
    'website' : '',
    'depends' : ['mail', 'gbs_stock_product', 'stock_indent'],

    'data' : ['security/ir.model.access.csv',
            'views/indent_return_view.xml',
            ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

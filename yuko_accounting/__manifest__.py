
{
    'name' : 'Yuko Accounting',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Accounting',
    'description': """
    
    """,
    'category': '',
    'sequence': 4,
    'website' : '',
    'depends' : [
                 'account',
                 'account_budget',
                 'analytic', 'account_asset',
                 'yuko_employee_iou',
                 ],
    'data' : ['security/ir.model.access.csv',
              'views/account_view.xml',
               'views/inherit_account_menu.xml',
              'views/asset_category_type_views.xml',
             ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

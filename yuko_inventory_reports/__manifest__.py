
{
    'name' : 'Yuko Inventory Reports',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'Inventory',
    'description': """
    
    """,
    'category': '',
    'sequence': 4,
    'website' : '',
    'depends' : ['product', 'stock', 'stock_picking_extend', 'yuko_report_layout'],
    'data' : [
            "wizard/stock_move_wizard.xml",
            "report/stock_move_report.xml",
            ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

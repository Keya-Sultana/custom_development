{
    'name': 'Indent Management',
    'author': 'Odoo Bangladesh',
    'website': 'www.odoo.com.bd',
    'license': 'LGPL-3',
    'version': "15.0.1.0.0",
    'category': 'Warehouse Management',
    'description': """
Indent Management
===================
Usually big companies set-up and maintain internal requisition to be raised by Engineer, Plant Managers or Authorised Employees. Using Indent Management you can control the purchase and issue of material to employees within company warehouse.

- Purchase Indents
- Store purchase
- Capital Purchase
- Repairing Indents
- Project Costing
- Valuation
- etc.

Purchase Indents
++++++++++++++++++
When there is a need of specific materials or services, authorized employees or managers will create a Purchase Indent. He can specify required date, whether the indent is for store or capital, the urgency of materials etc. on indent.

While selecting the product, the system will automatically set the procure method based on the quantity on hand for the product. Once the indent is approved, an internal move has been generated. A purchase order will also be generated if the products are not in stock and to be purchased.


Repairing Indents
++++++++++++++++++
A store manager or will create a repairing indent when the product is needed to be sent for repairing. In case of repairing indent you will be able to select product to be repaired and service for repairing of the product.

A purchase order is generated for the service taken for the supplier who repairs the product, and an internal move has been created for the product to be moved for repairing.
    """,
    'depends': [
                # 'gbs_stock_product',
                'account',
                'stock',
                # 'ir_sequence_operating_unit',
                # 'indent_type',
                # 'gbs_product_category',
                # 'web.report_layout',
                'stock_operating_unit_user'
                ],
    'complexity': "normal",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'report/stock_indent_report.xml',
        'data/stock_indent_data.xml',
        'data/stock_indent_sequence.xml',
        'views/indent_type_views.xml',
        'views/inherited_product_category.xml',
        'views/stock_location_view.xml',
        'views/stock_indent_view.xml',
        'views/stock_indent_config_views.xml',
        ],
    'installable': True,
    'application': False,
}

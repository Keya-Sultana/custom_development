
{
    'name' : 'New Yuko Purchase',
    'version' : '1.0',
    'author' : 'Odoo Bangladesh',
    'summary': 'New Purchase',
    'description': """
    
    """,
    'category': '',
    'sequence': 3,
    'website' : '',
    'depends' : [
                "gbs_purchase_order",
                'purchase_requisition',
                'gbs_supplier',
                'gbs_purchase_requisition',
                'yuko_report_layout',
                'purchase_order_revision',
                ],
    'data' : [
                "security/security.xml",
                "security/ir.model.access.csv",
                "views/purchase_menu_view.xml",
                "views/res_partner_view.xml",
                "views/purchase_order_views.xml",
                "views/purchase_requisition_views.xml",
                "views/business_type_views.xml",
                "views/payment_type_views.xml",
                "views/shipping_method_views.xml",
                "views/shipping_port_views.xml",
                "views/template_type_views.xml",
                "reports/inherit_report_puschae_order.xml",
                "reports/inherit_purchase_quotation_templates.xml",
                # "reports/inherit_purchase_order_report.xml",
                "reports/inherit_gbs_purchase_requisition_report.xml",
             ],
    'auto_install': False,
    'application': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

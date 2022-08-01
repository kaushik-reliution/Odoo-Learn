{
    'name': 'Order Delivery Status',
    'version': '15.0',
    'summary': "Order Delivery Status",
    'sequence': "5",
    'description': """Sales beyond imagination """,
    'category': "productivity",
    'website': "www.reliution.com",
    'licence': "LGPL-3",
    'depends': ['crm', 'sale', 'product', 'stock', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sale_order_mail.xml',
        'report/s_order_report.xml',
        'wizard/sorder_report_wizard.xml',
        'views/sale_view.xml',
        'views/xls_report_views.xml',
        'report/report.xml',

    ],
    'application': True,
    'auto_install': False
}

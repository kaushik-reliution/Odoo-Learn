{
    'name': 'CRM',
    'version': '15.0',
    'summary': "Customer Relationship Management",
    'sequence': "5",
    'description': """Sales beyond imagination """,
    'category': "productivity",
    'website': "www.reliution.com",
    'licence': "LGPL-3",
    'depends': ['crm', 'sale','product','stock', 'account', 'mail'],
    'data': ['data/credit_limit_mail_template.xml',
             'security/ir.model.access.csv',
             'security/sale_security.xml',
             'wizard/credit_limit_wizard.xml',
             'views/crm_lead_view.xml',
             'views/sale_view.xml',
             'views/customer_credit_view.xml',
             'views/warehouse_view.xml',
             ],
    'application': True,
    'auto_install': False
}

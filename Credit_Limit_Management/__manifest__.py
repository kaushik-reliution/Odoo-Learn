{
    'name': 'Credit Limit',
    'version': '15.0',
    'summary': "Credit Limit Management App",
    'sequence': "5",
    'description': """Control Over Credit Limit """,
    'category': "productivity",
    'website': "www.reliution.com",
    'licence': "LGPL-3",
    'depends': ['sale','product','stock', 'account', 'mail'],
    'data': ['data/credit_limit_mail_template.xml',
             'security/ir.model.access.csv',
             'security/sale_security.xml',
             'wizard/credit_limit_wizard.xml',
             'views/sale_view.xml',
             'views/customer_credit_view.xml',
             ],
    'application': True,
    'auto_install': False
}

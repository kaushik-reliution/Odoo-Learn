{
    'name': 'Invoice Report',
    'version': '15.0',
    'summary': "invoice report",
    'sequence': "5",
    'description': """Sales beyond imagination """,
    'category': "productivity",
    'website': "www.reliution.com",
    'licence': "LGPL-3",
    'depends': ['sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/invoice_mail.xml',
        'report/report.xml',
        'report/invoice_summary_report.xml',
        'wizard/invoice_report_wizard.xml',
        'views/invoice_menu_view.xml',
    ],
    'application': True,
    'auto_install': False
}

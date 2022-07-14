# -*- coding: utf-8 -*-

{
    'name': 'Vat Report',
    'version': '',
    'summary': '',
    'sequence': 0,
    'description': """

    """,
    'depends': ['account', 'hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'report/vat_report.xml',
        'wizard/vat_report_wizard_views.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

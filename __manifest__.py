{
    'name': 'College ERP',
    'version': '19.0.1.0.6',
    'license': 'LGPL-3',
    'author': 'Najoom Al Thuraya',
    'website': 'https://althurayauae.com/',
    'category':'Education',
    'summary': 'An erp for college management',
    'description': """Form student admission to gradution, this cover all aspects of college management""",
    'sequence': -10,
    'application': True,
    'depends': ['base', 'contacts', 'account', 'sale', 'purchase','hr'],
    'installable': True,
    'data': [
        'security/college_erp_security.xml',
        'security/ir.model.access.csv',
        'views/college_students_views.xml',
        'views/college_erp_menus.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/hr_employee_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_company_views.xml',
        'views/accounting_views/report_invoice.xml',
        'views/accounting_views/account_move_views.xml',
        'data/ir_sequence_data.xml',
        'data/ir_sequence_sync.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'college_erp/static/src/scss/college_students_list.scss',
        ],
        'web.report_assets_common': [
            'college_erp/static/src/css/report_college_invoice.css',
        ],
        'web.report_assets_pdf': [
            'college_erp/static/src/css/report_college_invoice.css',
        ],
    },
}

{
    'name': 'College ERP',
    'version': '19.0.1.0.3',
    'license': 'LGPL-3',
    'author': 'Najoom Al Thuraya',
    'website': 'https://althurayauae.com/',
    'category':'Education',
    'summary': 'An erp for college management',
    'description': """Form student admission to gradution, this cover all aspects of college management""",
    'sequence': -10,
    'application': True,
    'depends': ['base','contacts'],
    'installable': True,
    'data': [
        'security/college_erp_security.xml',
        'security/ir.model.access.csv',
        'views/college_students_views.xml',
        'views/college_erp_menus.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'college_erp/static/src/scss/college_students_list.scss',
        ],
    },
}

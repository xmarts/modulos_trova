{
    'name': 'Trova Employee',
    'version': '1.0',
    'summary': 'Personalizacion de Trova',
    'description': 'Pagos por destajo',
    'category': 'Personalizacion',
    'author': 'Javier Hilario Dominguez',
    'website': 'www.xmarts.com',
    'depends': [
        'hr','trova_vivienda'
                ],
    'data': [
        'views/view.xml',
        'reports/report_menu.xml',
        'reports/report_pagos_destajo.xml',
        'reports/report_pagos_destajo2.xml',

    ],
    'installable': True,
    'auto_install': False,
}
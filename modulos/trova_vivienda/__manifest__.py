{
    'name': 'Vivienda',
    'version': '2.0',
    'summary': 'Personalizacion de Trova',
    'description': 'Modulo de viviendas',
    'category': 'Personalizacion',
    'author': 'William Colin Macedo',
    'website': 'www.xmarts.com',
    'depends': ['base', 'contacts','hr','sale'],
    'data': ['views/view.xml',
             'views/view_saneam.xml',
             'views/view_tit.xml',
             'views/view_paquete.xml',
             'views/view_notarias.xml',
             'views/view_evaluacion.xml',
             'reports/contrato_venta.xml',
             'reports/acta_recepcion.xml',
             'reports/datos_clientes.xml',
             'reports/evaluacion_vivienda.xml',             
             'reports/report_menu.xml',
             'reports/fraccionamiento.xml',
             'reports/liquidacion_cliente.xml',
             'reports/vivienda_garantia.xml',
             'reports/solicitud_compra.xml',
             'reports/avaluo_vivienda.xml',
             'reports/carta_notarial.xml'
            ],

    'installable': True,
    'aplication': True,
    'auto_install': False,
}



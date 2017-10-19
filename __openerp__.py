# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Record the number of times a product is rejected',
    'version': '9.0.1.0.2',
    'category': 'Sales',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': ['product', ],
    'data': [
        'views/product_rejected_view.xml',
        'views/res_company_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False
}

# -*- coding: utf-8 -*-
{
    'name': "Education",

    'summary': """
       Gestion de la planification des cours dans un établissement.""",

    'description': """
        Gestion des cours.
    """,

    'author': "LIONEL LEUMENI",
    'installable': True,
    'application': True,
    'category': 'Wise',
    'version': '1.0.0',
    'depends': ['calendar'],


    # always loaded
    'data': [
        'views/cours.xml',
        'views/enseignants.xml',
        'views/etudiants.xml', 
        # 'views/classes.xml', 
        'views/coordinations.xml', 
        'views/calendriers.xml',
        'data/ir_sequence_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/classe.xml',
        'views/niveau.xml',
        'views/utilisateur.xml',
        'views/menu.xml',
        
    ],
}
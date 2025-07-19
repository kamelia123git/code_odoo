{
    'name': 'Bon de Préparation',
    'version': '1.0',
    'summary': 'Gestion des bons de préparation avec workflow, wizard d\'impression et rapport personnalisé.',
    'sequence': 10,
    'category': 'Sales/Preparation',
    'depends': [
        'base',
        'product',
        'contacts',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/bon_preparation_wizard_views.xml',
        'views/bon_preparation_view.xml',
        'report/custom_layout.xml',
        'report/bon_preparation_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
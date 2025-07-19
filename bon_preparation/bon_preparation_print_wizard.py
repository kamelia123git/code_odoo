from odoo import fields, models, api

class BonPreparationPrintWizard(models.TransientModel):
    _name = 'bon.preparation.print.wizard'
    _description = "Assistant d'impression du Bon de Préparation"

    # Bon de préparation sélectionné
    bon_preparation_id = fields.Many2one(
        'bon.preparation',
        string="Bon de Préparation",
        required=True,
        default=lambda self: self._default_bon_preparation_id()
    )

    # Champs supplémentaires
    charged_by_id = fields.Many2one(
        'res.users',
        string='Chargé',
        required=True,
        default=lambda self: self.env.user
    )

    print_date = fields.Datetime(
        string='Date',
        required=True,
        default=lambda self: fields.Datetime.now()
    )

    delivery_company = fields.Selection([
        ('guepex', 'Guepex Express'),
        ('dhl', 'DHL'),
    ], string='Société de Livraison', default='guepex', required=True)

    # Défaut : récupérer le bon actif
    @api.model
    def _default_bon_preparation_id(self):
        active_id = self.env.context.get('active_id') or self.env.context.get('default_bon_preparation_id')
        return active_id

    # Bouton Imprimer
    def print_report(self):
        self.ensure_one()
        bon = self.bon_preparation_id
        if not bon:
            # Dernière tentative : chercher via contexte
            active_id = self.env.context.get('active_id') or self.env.context.get('default_bon_preparation_id')
            if active_id:
                bon = self.env['bon.preparation'].browse(active_id)
        if not bon:
            raise ValueError("Aucun bon de préparation sélectionné.")

        return self.env.ref('bon_preparation.action_report_bon_preparation').report_action(
            bon,
            data={
                'charged_by': self.charged_by_id.name,
                'print_datetime': self.print_date,
                'delivery_company': dict(self._fields['delivery_company'].selection).get(self.delivery_company),
            }
        )

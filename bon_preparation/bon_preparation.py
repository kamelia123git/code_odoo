# bon_preparation/models/bon_preparation.py

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BonPreparation(models.Model):
    _name = 'bon.preparation'
    _description = 'Bon de Préparation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('Nouveau'),
                       tracking=True)

    client_id = fields.Many2one('res.partner', string='Client', required=True,)
    # domain = [('client_preparation', '=', True)] # Laissé en commentaire comme demandé

    adresse = fields.Char(string='Adresse', compute='_compute_client_info', readonly=True, store=True)
    telephone = fields.Char(string='Tél', compute='_compute_client_info', readonly=True, store=True)
    product_ids = fields.One2many('bon.preparation.line', 'bon_preparation_id', string='Produits', copy=True)

    # NOUVEAU CHAMP AJOUTÉ : Date de Livraison
    delivery_date = fields.Date(string='Date de Livraison') # Ou fields.Datetime si vous avez besoin de l'heure

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
    ], string='Statut', default='draft', copy=False, readonly=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('Nouveau')) == _('Nouveau'):
            vals['name'] = self.env['ir.sequence'].next_by_code('bon.preparation.sequence') or _('Nouveau')
        result = super(BonPreparation, self).create(vals)
        return result

    @api.depends('client_id')
    def _compute_client_info(self):
        for rec in self:
            if rec.client_id:
                address_parts = []
                if rec.client_id.street:
                    address_parts.append(rec.client_id.street)
                if rec.client_id.zip:
                    address_parts.append(rec.client_id.zip)
                if rec.client_id.city:
                    address_parts.append(rec.client_id.city)
                rec.adresse = ', '.join(address_parts) if address_parts else False
                rec.telephone = rec.client_id.phone
            else:
                rec.adresse = False
                rec.telephone = False

    def action_validate(self):
        self.ensure_one()
        self.state = 'validated'


class BonPreparationLine(models.Model):
    _name = 'bon.preparation.line'
    _description = 'Ligne de Bon de Préparation'

    bon_preparation_id = fields.Many2one('bon.preparation', string='Bon de Préparation', required=True,
                                         ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Produit', required=True)
    product_default_code = fields.Char(string='Référence Produit', related='product_id.default_code', readonly=True,
                                       store=True)
    quantity = fields.Float(string='Quantité', required=True, default=1.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_default_code = self.product_id.default_code
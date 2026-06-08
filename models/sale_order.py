from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Only customers appear in the Customer field on quotations/orders.
    partner_id = fields.Many2one(domain="[('contact_type', '=', 'customer')]")

    # Related field for list/kanban views (e.g. CUST/00001 next to customer name).
    customer_id = fields.Char(
        string='Customer ID',
        related='partner_id.customer_id',
        readonly=True,
    )

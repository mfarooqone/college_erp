from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
        ('company', 'Company'),
    ], string='Contact Type', required=True)

    customer_id = fields.Char(string='Customer ID', readonly=True, copy=False)
    vendor_id = fields.Char(string='Vendor ID', readonly=True, copy=False)

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if 'contact_type' not in fields_list:
            return values

        search_mode = self.env.context.get('res_partner_search_mode')
        if search_mode == 'customer':
            values['contact_type'] = 'customer'
        elif search_mode == 'supplier':
            values['contact_type'] = 'vendor'

        return values

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        for partner in partners:
            if partner.contact_type == 'customer' and not partner.customer_id:
                partner.customer_id = self.env['ir.sequence'].next_by_code('customer.id')
            elif partner.contact_type == 'vendor' and not partner.vendor_id:
                partner.vendor_id = self.env['ir.sequence'].next_by_code('vendor.id')
        return partners

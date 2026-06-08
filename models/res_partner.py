from odoo import api, fields, models


class ResPartner(models.Model):
    """Extend contacts with a type and auto-generated IDs (CUST/, VEND/, EMP/)."""
    _inherit = 'res.partner'

    # Classifies each contact so Sales/Purchase/HR can filter the right partners.
    contact_type = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
        ('company', 'Company'),
    ], string='Contact Type', required=True)

    # Stored on res.partner; assigned once on create from ir.sequence (see data/ir_sequence_data.xml).
    customer_id = fields.Char(string='Customer ID', readonly=True, copy=False)
    vendor_id = fields.Char(string='Vendor ID', readonly=True, copy=False)
    employee_id = fields.Char(string='Employee ID', readonly=True, copy=False)

    # Single ID column for the Contacts app (CUST/, VEND/, or EMP/ depending on type).
    contact_code = fields.Char(
        string='ID',
        compute='_compute_contact_code',
    )

    @api.depends('contact_type', 'customer_id', 'vendor_id', 'employee_id')
    def _compute_contact_code(self):
        for partner in self:
            if partner.contact_type == 'customer':
                partner.contact_code = partner.customer_id
            elif partner.contact_type == 'vendor':
                partner.contact_code = partner.vendor_id
            elif partner.contact_type == 'employee':
                partner.contact_code = partner.employee_id
            else:
                partner.contact_code = False

    @api.model
    def default_get(self, fields_list):
        """Pre-fill contact_type from the menu that opened the form."""
        values = super().default_get(fields_list)
        if 'contact_type' not in fields_list:
            return values

        search_mode = self.env.context.get('res_partner_search_mode')
        if search_mode == 'customer':
            values['contact_type'] = 'customer'
        elif search_mode == 'supplier':
            # Purchase app uses 'supplier' in context; we store it as 'vendor'.
            values['contact_type'] = 'vendor'
        elif self.env.context.get('default_contact_type') == 'employee':
            values['contact_type'] = 'employee'
        return values

    @api.model_create_multi
    def create(self, vals_list):
        """Assign the matching sequence code after the contact is saved."""
        partners = super().create(vals_list)
        for partner in partners:
            if partner.contact_type == 'customer' and not partner.customer_id:
                partner.customer_id = self.env['ir.sequence'].next_by_code('customer.id')
            elif partner.contact_type == 'vendor' and not partner.vendor_id:
                partner.vendor_id = self.env['ir.sequence'].next_by_code('vendor.id')
            elif partner.contact_type == 'employee' and not partner.employee_id:
                partner.employee_id = self.env['ir.sequence'].next_by_code('employee.id')
        return partners

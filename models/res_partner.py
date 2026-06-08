from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = ['res.partner', 'college.erp.contact.id.mixin']

    _customer_id_unique = models.Constraint('UNIQUE (customer_id)', 'Customer ID must be unique.')
    _vendor_id_unique = models.Constraint('UNIQUE (vendor_id)', 'Vendor ID must be unique.')
    _employee_id_unique = models.Constraint('UNIQUE (employee_id)', 'Employee ID must be unique.')

    contact_type = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
        ('company', 'Company'),
    ], string='Contact Type', required=True)

    customer_id = fields.Char(string='Customer ID', readonly=True, copy=False)
    vendor_id = fields.Char(string='Vendor ID', readonly=True, copy=False)
    employee_id = fields.Char(string='Employee ID', readonly=True, copy=False)
    contact_code = fields.Char(string='ID', compute='_compute_contact_code')

    @api.depends('contact_type', 'customer_id', 'vendor_id', 'employee_id')
    def _compute_contact_code(self):
        for partner in self:
            field = self._contact_id_field(partner.contact_type)
            partner.contact_code = partner[field] if field else False

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if 'contact_type' not in fields_list:
            return values
        if self.env.context.get('res_partner_search_mode') == 'customer':
            values['contact_type'] = 'customer'
        elif self.env.context.get('res_partner_search_mode') == 'supplier':
            values['contact_type'] = 'vendor'
        elif self.env.context.get('default_contact_type') == 'employee':
            values['contact_type'] = 'employee'
        return values

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            contact_type = vals.get('contact_type')
            field = self._contact_id_field(contact_type)
            if field and not vals.get(field):
                vals[field] = self._next_contact_id(contact_type)
        return super().create(vals_list)

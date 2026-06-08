from odoo import fields, models
from odoo.exceptions import UserError
from odoo import _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Named employee_code (not employee_id) because hr.employee already has an employee_id field.
    # Value comes from the linked work contact's EMP/ sequence (set in res.partner.create).
    employee_code = fields.Char(
        string='Employee ID',
        related='work_contact_id.employee_id',
        readonly=True,
    )

    def _create_work_contacts(self):
        """Create work contacts as employee-type partners so they get an EMP/ ID."""
        if any(employee.work_contact_id for employee in self):
            raise UserError(_('Some employee already have a work contact'))

        work_contacts = self.env['res.partner'].create([{
            'email': employee.work_email,
            'phone': employee.work_phone,
            'name': employee.name,
            'image_1920': employee.image_1920,
            'company_id': employee.company_id.id,
            'contact_type': 'employee',  # triggers employee.id sequence on res.partner
        } for employee in self])

        for employee, work_contact in zip(self, work_contacts):
            employee.work_contact_id = work_contact
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_ids = fields.One2many('college.students', 'partner_id', string='Students')
    student_count = fields.Integer(compute='_compute_student_count')

    def _compute_student_count(self):
        for partner in self:
            partner.student_count = len(partner.student_ids)

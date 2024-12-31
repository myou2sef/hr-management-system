from odoo import models, fields, api, _

class HrDepartment(models.Model):
    _name = 'hr.department'
    _description = 'Department'
    _inherit = ['mail.thread']
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string='Department Name', required=True, tracking=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    parent_id = fields.Many2one('hr.department', string='Parent Department', index=True)
    child_ids = fields.One2many('hr.department', 'parent_id', string='Child Departments')
    parent_path = fields.Char(index=True)
    
    manager_id = fields.Many2one('hr.employee', string='Manager')
    member_ids = fields.One2many('hr.employee', 'department_id', string='Members')
    jobs_ids = fields.One2many('hr.position', 'department_id', string='Jobs')
    note = fields.Text(string='Note')
    
    color = fields.Integer(string='Color Index')
    code = fields.Char(string='Department Code', required=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive departments.'))

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result

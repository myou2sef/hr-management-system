from odoo import models, fields, api, _

class HrPosition(models.Model):
    _name = 'hr.position'
    _description = 'Job Position'
    _inherit = ['mail.thread']

    name = fields.Char(string='Job Position', required=True, tracking=True)
    code = fields.Char(string='Position Code', required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Job Description')
    requirements = fields.Text(string='Requirements')
    
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    employee_ids = fields.One2many('hr.employee', 'position_id', string='Employees')
    no_of_employees = fields.Integer(compute='_compute_employees', string="Current Number of Employees")
    expected_employees = fields.Integer(string='Expected Number of Employees', copy=False)
    no_of_recruitment = fields.Integer(string='Expected New Employees', copy=False)
    no_of_hired_employee = fields.Integer(string='Hired Employees', copy=False)
    
    grade_level = fields.Selection([
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Team Lead'),
        ('manager', 'Manager'),
        ('director', 'Director'),
    ], string='Grade Level', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting'),
        ('closed', 'Closed')
    ], string='Status', required=True, tracking=True, copy=False, default='draft')

    @api.depends('employee_ids')
    def _compute_employees(self):
        for position in self:
            position.no_of_employees = len(position.employee_ids)

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result
        
    def action_start_recruitment(self):
        self.write({'state': 'recruit'})

    def action_close_recruitment(self):
        self.write({'state': 'open'})

    def action_close_position(self):
        self.write({'state': 'closed'})

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('hr.position') or _('New')
        return super(HrPosition, self).create(vals)

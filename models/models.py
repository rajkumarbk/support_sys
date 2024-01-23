from odoo import models, fields, api
from datetime import datetime


class support_sys(models.Model):
    _name = 'support_sys.support_sys'
    _description = 'support_sys.support_sys'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    c_id = fields.Integer(string='ID', tracking=True)
    name = fields.Char(string='Client Name', tracking=True)
    image = fields.Binary("Client Image", tracking=True)
    issue_description = fields.Char(string='Issued Description', tracking=True)
    support_type = fields.Selection([
        ('ordinary', 'Ordinary'),
        ('vip', 'VIP')
    ], string='Support Type', default='ordinary', help='Select the support type', tracking=True)
    assigned_employee = fields.Char(string='Name of Employee', tracking=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ], string='Status', default='new', tracking=True)
    month_field = fields.Date(
        string='Date',
        widget='Date',
        help='Select a month',
        default=datetime.now().date(), tracking=True
    )
    day_field = fields.Integer(
        string='Day',
        compute='_compute_day_month_year',
        store=True
    )
    months_field = fields.Integer(
        string='Month',
        compute='_compute_day_month_year',
        store=True
    )
    year_field = fields.Integer(
        string='Year',
        compute='_compute_day_month_year',
        store=True
    )

    @api.depends('month_field')
    def _compute_day_month_year(self):
        for record in self:
            record.day_field = record.month_field.day if record.month_field else False
            record.months_field = record.month_field.month if record.month_field else False
            record.year_field = record.month_field.year if record.month_field else False


class Ticket(models.Model):
    _name = 'ticket.raise'
    _description = 'ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ticket_id = fields.Char(string='Ticket ID')
    ticket_type = fields.Selection(
        [('complain', 'Complain'), ('feedback', 'Feedback'), ('request', 'Request'), ('query', 'Query')],
        string='Ticket Type', tracking=True)
    product = fields.Selection([('Internet', 'Internet'), ('Software', 'Software'), ('Website', 'Website')
                                ],
                               string='Choose a Product')
    message = fields.Text(string='Message', required=True)
    priority = fields.Selection([('urgent', 'Urgent'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
                                string='Priority', tracking=True)
    status = fields.Selection(
        [('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='New', String="Progress", required=True, tracking=True)
    photo = fields.Binary(string='photo', tracking=True)
    nepalidatepicker = fields.Date(string='Requested date', required=True, tracking=True)
    client_email = fields.Char(string='Client Email', tracking=True)
    # assigned_department_id = fields.Many2one('hr.employee',string='Assigned Department', tracking=True)
    department_id = fields.Many2one(
        'hr.department',  # Replace with the actual model name for employees
        string='Assigned Department'
    )
    name_id = fields.Many2one(
        'hr.employee',  # Replace with the actual model name for employees
        string='AssignedEmployee'
    )
    # photo_filename = fields.Char(string='photo Filename')

    def action_confirm(self):
        for ticket in self:
            employee = ticket.name_id
            if employee:
                employee.write({'problem': ticket.message})
                employee.write({'Title': ticket.ticket_type})
                employee.write({'Ticket_num': ticket.ticket_id})
                employee.write({'e_priority': ticket.priority})
                employee.write({'e_image': ticket.photo})
        self.write({'status':'In Progress'})

    def action_decline(self):
        self.write({'status': 'Cancelled'})

    def action_completed(self):
        self.write({'status': 'Completed'})

    @api.onchange('department_id')
    def on_department_change(self):
        if self.department_id:
            employees = self.env['hr.employee'].search([('department_id', '=', self.department_id.id)])
            return {'domain': {'name_id': [('id', 'in', employees.ids)]}}
        else:
            return {'domain': {'name_id':[]}}

    @api.model
    def create(self, vals):
        print("Sequence", vals)
        vals['ticket_id'] = self.env['ir.sequence'].next_by_code("ticket.raise")
        return super(Ticket, self).create(vals)


class Employee(models.Model):
    _description = 'employee'
    _inherit = ['hr.employee']
    # _name = 'employee.details'

    is_available = fields.Boolean("Is Available?")

    employee_id = fields.Char(string='Sequence Number')
    employee_name = fields.Char(string='Employee Name', tracking=True)
    contact = fields.Char(tracking=True)
    address = fields.Char(tracking=True)
    department = fields.Char(tracking=True)
    position = fields.Char(tracking=True)
    salary = fields.Integer(tracking=True)
    date_joined = fields.Date(tracking=True)
    _sql_constraints = [
        ('employee_id_uniq', 'unique(employee_id)', 'Employee ID must be unique!'),
    ]

    @api.model
    def create(self, vals):
        print("Sequence", vals)
        vals['employee_id'] = self.env['ir.sequence'].next_by_code("employee.details")
        return super(Employee, self).create(vals)


class Expense(models.Model):
    _name = 'employee.expense'
    _description = 'employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    nepalidatepicker = fields.Date(string='Expense Date', default=fields.Date.today())
    amount = fields.Float(string='Amount', default=None)
    description = fields.Text(string='Description')
    expense_category = fields.Selection([
        ('Meals', 'Meals'),
        ('Travel', 'Travel'),
        ('Accomodation', 'Accomodation'),
        ('Other', 'Other'),
    ], string='Expense Category', tracking=True)
    status = fields.Selection(
        [('New', 'New'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='New', String="Progress", required=True, tracking=True)
    starting_location = fields.Char(string='Starting Location', tracking=True)
    ending_location = fields.Char(string='Ending Location', tracking=True)

    photo = fields.Binary("Bill Image", tracking=True)
    hotel_name = fields.Char("Hotel Name")
    hotel_address = fields.Char("Address", tracking=True)
    hotel_phone = fields.Char("Phone", tracking=True)

    def action_accepted(self):
        self.write({'status': 'Accepted'})

    def action_rejected(self):
        self.write({'status': 'Rejected'})

    def submit_ticket(self):
        return {'type': 'ir.actions.act_window_close'}

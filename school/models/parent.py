# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ParentRelation(models.Model):
    """Defining a Parent relation with child."""

    _name = "parent.relation"
    _description = "Parent-child relation information"

    name = fields.Char(
        "Relation name", required=True, help="Parent relation with student"
    )
    

class SchoolParent(models.Model):
    """Defining a Teacher information."""

    _name = "school.parent"
    _description = "Parent Information"

    partner_id = fields.Many2one(
        "res.partner",
        "User ID",
        ondelete="cascade",
        delegate=True,
        required=True,
        help="Partner which is user over here",
    )
    id_partner_1 = fields.Char(
            "ID Partner",
            help="Enter ID Partner",
    )
    relation_id = fields.Many2one(
        "parent.relation",
        "Relation with Child",
        help="Parent relation with child",
    )
    student_id = fields.Many2many(
        "student.student",
        "students_parents_rel",
        "students_parent_id",
        "student_id",
        "Children",
        help="Student of the following parent",
    )
    standard_id = fields.Many2many(
        "school.standard",
        "school_standard_parent_rel",
        "class_parent_id",
        "class_id",
        "Academic Class",
        help="""Class of the student of following parent""",
    )
    stand_id = fields.Many2many(
        "standard.standard",
        "standard_standard_parent_rel",
        "standard_parent_id",
        "standard_id",
        "Academic Standard",
        help="""Standard of the student of following parent""",
    )
    teacher_id = fields.Many2one(
        "school.teacher",
        "Teacher",
        store=True,
        related="standard_id.user_id",
        help="Teacher of a student",
    )
    
    create_date_id = fields.Date(
            "Create Date",
            help="Enter create date",
    )
    home_number = fields.Char(
            "Home number",
            help="Enter Home number",
    )
    
    SMS_phone = fields.Char(
            "SMS Phone",
            help="Enter SMS Phone",
    )
    International_phone = fields.Char(
            "SMS Phone",
            help="Enter International Phone",
    )
    father_nat_id = fields.Char(
            "Father National ID",
            help="Enter Father National ID",
    )
    job_position = fields.Char(
            "Job positionr",
            help="Enter Job position",
    )
    specialty = fields.Char(
            "Specialty",
            help="Enter Specialty",
    )
    Educational_level = fields.Char(
            "Educational level",
            help="Enter Educational level",
    )
    name_arabic_1 = fields.Char(
            "First Name in Arabic",
            required=True,
            
            help="Enter student name in Arabic",
    )
    name_arabic_2 = fields.Char(
            "Second Name in Arabic",
            required=True,
            help="Enter student name in Arabic",
    )
    name_arabic_3 = fields.Char(
            "Third Name in Arabic",
            required=True,
            help="Enter student name in Arabic",
    )
    name_arabic_4 = fields.Char(
            "Family Name in Arabic",
            required=True,
            help="Enter student name in Arabic",
    )
    name_en_1 = fields.Char(
            "First Name in English",
            required=True,
            help="Enter student name in English",
    )
    name_en_2 = fields.Char(
            "Second Name in English",
            required=True,
            help="Enter student name in English",
    )
    name_en_3 = fields.Char(
            "Third Name in English",
            required=True,
            help="Enter student name in English ",
    )
    name_en_4 = fields.Char(
            "Family Name in English",
            required=True,
            help="Enter student name in English ",
    )
    status = fields.Char(
            "Family Name in English",
            required=True,
            help="Enter status ",
    )
    nationality = fields.Char(
            "Family nationality",
            required=True,
            help="Enter nationality ",
    )
    working_address = fields.Char(
            "Family Name in English",
            required=True,
            help="Enter working address ",
    )




    @api.onchange("student_id")
    def onchange_student_id(self):
        """Onchange Method for Student."""
        standard_ids = self.student_id.mapped("standard_id")
        if standard_ids:
            self.standard_id = [(6, 0, standard_ids.ids)]
            self.stand_id = [(6, 0, standard_ids.mapped("standard_id").ids)]

    @api.model
    def create(self, vals):
        """Inherited create method to assign values in
        the users record to maintain the delegation"""
        res = super(SchoolParent, self).create(vals)
        parent_grp_id = self.env.ref("school.group_school_parent")
        emp_grp = self.env.ref("base.group_user")
        self.env["res.users"].create(
            {
                "name": res.name,
                "login": res.email,
                "email": res.email,
                "partner_id": res.partner_id.id,
                "groups_id": [(6, 0, [emp_grp.id, parent_grp_id.id])],
            }
        )
        return res

    @api.onchange("state_id")
    def onchange_state(self):
        """Onchange Method for State."""
        if self.state_id:
            self.country_id = self.state_id.country_id.id or False

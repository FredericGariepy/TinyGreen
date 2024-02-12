import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, TimeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Optional
from tinyGreen.models import User

class RegisterForm(FlaskForm):

    # !!! Magic
    # FlaskForm will handle the function itself
    # and after validate_... will look for a field type with the name 'username'
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email_address(self, email_to_check):
        email_address = User.query.filter_by(email_address=email_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already in use')


    username = StringField(label='User Name', validators=[Length(min=4,max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:',validators=[Length(min=6, max=30), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')
    
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')

class TeacherProfileForm(FlaskForm):
    
    nativeEnglish = [
        ('1',"Yes, I am a native English speaker"),
        ('2', "No, I am not an native English speaker")
    ]
    isNativeEnglish = SelectField('Are you a native English speaker?', choices=nativeEnglish, validators=[DataRequired()])

    experience_choices = [
        (1, '1 year'),
        (2,'2-3 years',),
        (3,'More than 3 years'), 
        (0,'No experience')
    ]
    yearsOfExperience = SelectField('Years of Experience', choices=experience_choices, validators=[DataRequired()])

    visa_types = [
    ("E-2", "E-2 Foreign language instructor"),
    ("Tourist", "Tourist Visa"),
    ("Outside Korea", "Not currently in Korea"),
    ("F-6", "F-6 Marriage to Korean Citizen"),
    ("H-1", "H-1 Working holiday"),
    ("F-1", "F-1 Visiting or joining family"),
    ("F-2", "F-2 Resident"),
    ("F-3", "F-3 Accompanying spouse / child"),
    ("F-4", "F-4 Overseas Korean"),
    ("F-5", "F-5 Permanent resident"),
    ("F-4-11", "F-4-11 Descendant of Overseas Korean"),
    ("F-4-13", "F-4-13 Former D or E visa holder"),
    ]
    visaType = SelectField("Visa Type",choices=visa_types, validators=[DataRequired()])
    
    contact_email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])

    submit = SubmitField(label="Create teacher profile")

class RecruiterProfileForm(FlaskForm):
    contact_email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    submit = SubmitField(label="Create Recruiter profile")

class JobForm(FlaskForm):
    
    title = StringField(label='Post Title', validators=[DataRequired(), Length(max=60)])
    
    job_type_choices = [
        ("Full-Time","Full-Time"),
        ("Part-Time","Part-Time"),
        ("Tutoring","Tutoring"),
        ("Substitute","Substitute"),
        ("Camp","Camp"),
        ("Library","Library"),
        ("Event","Event"),
        ("Non-Teaching","Non-Teaching"),
    ]
    job_type = SelectField(label='Job Type', choices=job_type_choices, validators=[DataRequired(), Length(max=40)])

    location_choices = [
    ("Seoul", "Seoul"),
    ("Busan", "Busan"),
    ("Daegu", "Daegu"),
    ("Incheon", "Incheon"),
    ("Gwangju", "Gwangju"),
    ("Daejeon", "Daejeon"),
    ("Ulsan", "Ulsan"),
    ("Gyeonggi-do", "Gyeonggi-do"),
    ("Gangwon-do", "Gangwon-do"),
    ("Chungcheongbuk-do", "Chungcheongbuk-do"),
    ("Chungcheongnam-do", "Chungcheongnam-do"),
    ("Jeollabuk-do", "Jeollabuk-do"),
    ("Jeollanam-do", "Jeollanam-do"),
    ("Gyeongsangbuk-do", "Gyeongsangbuk-do"),
    ("Gyeongsangnam-do", "Gyeongsangnam-do"),
    ("Jeju-do", "Jeju-do")
    ]
    location = SelectField(label='Location',choices=location_choices, validators=[DataRequired()])
    location_details = StringField(label='Location details', validators=[DataRequired(), Length(max=80)])
    
    salary = IntegerField(label='Salary', validators=[DataRequired()])
    salary_type_choices = [
        ('Month', 'Monthly'),
        ('Hour', 'Hourly'),
        ('Day', 'Daily'),
        ('Year', 'Yearly'),
        ('In Total', 'Lump Sum')
    ]
    salary_payment_type = SelectField(choices=salary_type_choices, validators=[DataRequired()])
    salary_negotiable = BooleanField(label='negotiable', default=False)

    startdate = DateField(label='Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    asap = BooleanField(label='As Soon As Possible (ASAP)', default=False)

    # Type of students
    kind_student = BooleanField(label='Kindergarten', default=False)
    elem_student = BooleanField(label='Elementary School', default=False)
    midl_student = BooleanField(label='Middle School', default=False)
    high_student = BooleanField(label='High School', default=False)
    univ_student = BooleanField(label='University', default=False)
    adlt_student = BooleanField(label='Adults', default=False)

    health_insurance = BooleanField(label='Health Insurance', default=False)
    pension = BooleanField(label='Pension Contribution', default=False)
    airfare = BooleanField(label='Airfare Reimbursement', default=False)
    severance = BooleanField(label='Severance', default=False)
    housing = BooleanField(label='Housing Provided', default=False)
    housing_allowance = IntegerField(label='Housing Allowance', validators=[Optional()])
    vacation_days = IntegerField(label='Vacation Days', validators=[Optional()])

    #WorkScheduleForm section (insted of using two forms) 
    # handled is handled in the route on submmit
    everyday_start_time = TimeField('Everyday Start Time', format='%H:%M', validators=[Optional()])
    everyday_end_time = TimeField('Everyday End Time', format='%H:%M', validators=[Optional()])

    monday_start_time = TimeField('Monday Start Time', format='%H:%M', validators=[Optional()])
    monday_end_time = TimeField('Monday End Time', format='%H:%M', validators=[Optional()])

    tuesday_start_time = TimeField('Tuesday Start Time', format='%H:%M', validators=[Optional()])
    tuesday_end_time = TimeField('Tuesday End Time', format='%H:%M', validators=[Optional()])

    wednesday_start_time = TimeField('Wednesday Start Time', format='%H:%M', validators=[Optional()])
    wednesday_end_time = TimeField('Wednesday End Time', format='%H:%M', validators=[Optional()])

    thursday_start_time = TimeField('Thursday Start Time', format='%H:%M', validators=[Optional()])
    thursday_end_time = TimeField('Thursday End Time', format='%H:%M', validators=[Optional()])

    friday_start_time = TimeField('Friday Start Time', format='%H:%M', validators=[Optional()])
    friday_end_time = TimeField('Friday End Time', format='%H:%M', validators=[Optional()])

    saturday_start_time = TimeField('Saturday Start Time', format='%H:%M', validators=[Optional()])
    saturday_end_time = TimeField('Saturday End Time', format='%H:%M', validators=[Optional()])

    sunday_start_time = TimeField('Sunday Start Time', format='%H:%M', validators=[Optional()])
    sunday_end_time = TimeField('Sunday End Time', format='%H:%M', validators=[Optional()])

    description = TextAreaField(
        label='Description',
        validators=[Optional(), Length(max=500)],
        render_kw={"maxlength": 500}
    )
    #date_posted is handled in the route on submmit
    submit = SubmitField(label='Post Job')

class QuickApplyJob(FlaskForm):
    submit = SubmitField(label='Apply now!')

class JobFilterForm(FlaskForm):
    title = StringField('Title', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])

    submit = SubmitField('Search')
    
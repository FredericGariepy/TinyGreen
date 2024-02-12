from datetime import datetime
from tinyGreen import db
from tinyGreen import bcrypt
from tinyGreen import login_manager
from flask_login import UserMixin

#https://flask-login.readthedocs.io/en/latest/#how-it-works
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30), nullable=False,unique=True)
    email_address = db.Column(db.String(length=50), nullable=False,unique=True)
    email_confirmed_date = db.Column(db.DateTime(),nullable=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=0)
    isTeacher = db.Column(db.Boolean(), nullable=True, default=None)
    
    items = db.relationship('Item',backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password) #returns true OR false

    def allowed_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def allowed_sell(self, item_obj):
        return item_obj in self.items #learn this logic better
    
    def set_default_teacher_budget(self):
        self.budget = 3

    def set_default_recruiter_budget(self):
        self.budget = 1
    
    def minus_budget(self, int):
        self.budget -= int

    def add_budget(self, int):
        self.budget += int

class TeacherProfile(db.Model):
    __tablename__ = 'teacher_profiles'

     # The primary key is also a foreign key to the User model
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    nativeEnglish = db.Column(db.Boolean, nullable=False)
    yearsOfExperience = db.Column(db.Integer, nullable=False)
    visaType = db.Column(db.String(10), nullable=False)
    contact_email_address = db.Column(db.String(length=50), nullable=False,unique=True)

    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False, lazy=True))

class RecruiterProfile(db.Model):
    __tablename__ = 'recruiter_profiles'

    # The primary key is also a foreign key to the User model
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    contact_email_address = db.Column(db.String(length=50), nullable=False,unique=True)
    
    user = db.relationship('User', backref=db.backref('recruiter_profiles', uselist=False, lazy=True))

class JobPost(db.Model):
    __tablename__ = 'job_post'

    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(length=60),nullable=False,unique=False)
    job_type = db.Column(db.String(length=40),nullable=False,unique=False)

    location = db.Column(db.String(length=40),nullable=False,unique=False)
    location_details = db.Column(db.String(length=80),nullable=True,unique=False)

    startdate = db.Column(db.Date, nullable=True)
    asap = db.Column(db.Boolean, nullable=True, default=False)
    
    kind_student = db.Column(db.Boolean, nullable=False, default=False)
    elem_student = db.Column(db.Boolean, nullable=False, default=False)
    midl_student = db.Column(db.Boolean, nullable=False, default=False)
    high_student = db.Column(db.Boolean, nullable=False, default=False)
    univ_student = db.Column(db.Boolean, nullable=False, default=False)
    adlt_student = db.Column(db.Boolean, nullable=False, default=False)

    health_insurance = db.Column(db.Boolean, nullable=False, default=False)
    pension = db.Column(db.Boolean, nullable=False, default=False)
    airfare = db.Column(db.Boolean, nullable=False, default=False)
    severance = db.Column(db.Boolean, nullable=False, default=False)
    housing = db.Column(db.Boolean, nullable=False, default=False)
    housing_allowance = db.Column(db.Integer(), nullable=True)
    vacation_days = db.Column(db.Integer(), nullable=True)

    salary = db.Column(db.Integer(), nullable=False)
    salary_negotiable = db.Column(db.Boolean, nullable=False, default=False)
    salary_payment_type = db.Column(db.String(length=80),nullable=False,unique=False)

    description = db.Column(db.String(length=500),nullable=True,unique=False)
    
    # date posted is handled automatically by default=datetime.utcnow
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    recruiter_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    recruiter = db.relationship('User', backref='job_posts', lazy=True)

    # one-to-one relationship with WorkSchedule
    work_schedule_id = db.Column(db.Integer(), db.ForeignKey('work_schedule.id'), unique=True, nullable=True)
    work_schedule = db.relationship('WorkSchedule', backref='job_post', uselist=False)

    # one-to-many
    applicants = db.relationship('JobApplicant', backref='job_post', uselist=True)


    def apply(self, user):
        new_applicant = JobApplicant(
            job_post_id = self.id,
            teacher_id = user.id
        )
        db.session.add(new_applicant)
        db.session.commit()

class WorkSchedule(db.Model):
    __tablename__ = 'work_schedule'

    id = db.Column(db.Integer(), primary_key=True)
    
    everyday_start_time = db.Column(db.Time, nullable=True)
    everyday_end_time = db.Column(db.Time, nullable=True)

    monday_start_time = db.Column(db.Time, nullable=True)
    monday_end_time = db.Column(db.Time, nullable=True)

    tuesday_start_time = db.Column(db.Time, nullable=True)
    tuesday_end_time = db.Column(db.Time, nullable=True)

    wednesday_start_time = db.Column(db.Time, nullable=True)
    wednesday_end_time = db.Column(db.Time, nullable=True)

    thursday_start_time = db.Column(db.Time, nullable=True)
    thursday_end_time = db.Column(db.Time, nullable=True)

    friday_start_time = db.Column(db.Time, nullable=True)
    friday_end_time = db.Column(db.Time, nullable=True)

    saturday_start_time = db.Column(db.Time, nullable=True)
    saturday_end_time = db.Column(db.Time, nullable=True)

    sunday_start_time = db.Column(db.Time, nullable=True)
    sunday_end_time = db.Column(db.Time, nullable=True)

class JobApplicant(db.Model):
    __tablename__ = 'job_applicants'

    id = db.Column(db.Integer, primary_key=True)
    job_post_id = db.Column(db.Integer, db.ForeignKey('job_post.id'))
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher_profiles.id'))
    is_shortlisted = db.Column(db.Boolean(), nullable=True, default=None)

class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    barcode =  db.Column(db.String(length=12), nullable=False,unique=True)
    description =  db.Column(db.String(length=120), nullable=False,unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()


    def __repr__(self):
        return f'Item {self.name}'
    

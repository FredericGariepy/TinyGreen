from sqlite3 import IntegrityError
from tinyGreen import app, db
from flask import render_template, redirect, url_for,flash, request
from tinyGreen.models import Item, RecruiterProfile, User, TeacherProfile,JobPost,JobApplicant, WorkSchedule
from tinyGreen.forms import JobFilterForm, JobForm, QuickApplyJob, RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, TeacherProfileForm,RecruiterProfileForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import joinedload

from datetime import datetime

# this could be a nice way to cache css
#@app.route('/static/css/styles.css')
#def static_file(filename):
#    cache_timeout = 600  # in seconds
#    return send_from_directory(os.path.join(app.root_path, 'static'), filename, cache_timeout=cache_timeout)

@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/')
@app.route('/job_board',methods=['GET','POST'])
def job_board_page():

    filter_form = JobFilterForm()
    job_posts_query = JobPost.query

    #this is to filter the jobs by title and location
    if request.method == "POST" and filter_form.validate_on_submit():
        if filter_form.title.data:
            job_posts_query = job_posts_query.filter(JobPost.title.ilike('%' + filter_form.title.data + '%'))
        if filter_form.location.data:
            job_posts_query = job_posts_query.filter(JobPost.location.ilike('%' + filter_form.location.data + '%'))

    job_posts = job_posts_query.order_by(JobPost.date_posted.desc()).all()
    # Create a variable for the current date and time
    current_datetime = datetime.now()

    return render_template("job_board.html", job_posts = job_posts, filter_form=filter_form, current_datetime=current_datetime)

@app.route('/job_post/<int:job_post_id>',methods=['GET','POST'])
def job_post(job_post_id):

    # Fetch specific job post
    job_post = JobPost.query.get(job_post_id)

    # Check if the job does not exist
    if job_post is None:
        flash('Job not available', 'info')
        return redirect(url_for('job_board_page'))
    
    # Fetch the recruiter profile associated with this job post
    recruiter_profile =  RecruiterProfile.query.get(job_post.recruiter_id)

    # mapping for students 
    student_type_mapping = {
        'elem_student': 'Elementary',
        'midl_student': 'Middle School',
        'high_student': 'High School',
        'univ_student': 'University',
        'adlt_student': 'Adult',
    }

    #there might be a better way... this is kinda rough
    existing_application = None  #Define existing_application before the if block
    try:
        if current_user.isTeacher:    
            existing_application = JobApplicant.query.filter_by(job_post_id = job_post_id, teacher_id = current_user.id).first()
    except:
        pass

    quick_apply_job = QuickApplyJob()
    if request.method == "POST":
        job_applied = request.form.get('job_applied') # job id retrieved from the 
        job_applied_object = JobPost.query.filter_by(id=job_applied).first()
        
        if current_user.isTeacher:
            #Check if Job exists
            if job_applied_object: 

                # Check if the user has already applied to the job
                if not existing_application:

                    if current_user.budget > 0:
                        current_user.minus_budget(1)
                        job_applied_object.apply(current_user)
                        flash(f'Successfully applied to {job_applied_object.title}', category='success')

                    else:flash(f'You ran out of Quick Apply tokens. Apply manually via email or get more tokens here.', category='warning')

                else:flash(f'You already applied to this job.', category='warning')

            else:flash(f'This Job does not exist anymore. Sorry for the inconvenience.', category='warning')

        else:flash(f'Recruiter may not apply to jobs', category='warning')

    return render_template("job_post.html", job_post=job_post, recruiter_profile=recruiter_profile, quick_apply_job=quick_apply_job,student_type_mapping=student_type_mapping, existing_application=existing_application)

@app.route('/job_post_applicants/<int:job_post_id>',methods=['GET'])
@login_required
def job_post_applicants(job_post_id):
    
    # Check if the current user is the recruiter who created the job post
    job_post = JobPost.query.get(job_post_id)
    
    if job_post.recruiter_id != current_user.id:
        flash('Access denied. You are not the recruiter for this job post.', 'warning')
        return redirect(url_for('home_page'))
    
    # Fetch job applicants for the specified job post
    job_applicants = (
        db.session.query(JobApplicant, TeacherProfile)
        .join(TeacherProfile, TeacherProfile.id == JobApplicant.teacher_id)
        .filter(JobApplicant.job_post_id == job_post_id)
        .options(joinedload(TeacherProfile.user))  # Apply joinedload to the relationship directly
        .all()
    )
    
    return render_template("job_post_applicants.html", job_post=job_post, job_applicants=job_applicants)


@app.route('/market',methods=['GET','POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form =  SellItemForm()

    if request.method == "POST":

        #purchase item logic
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.allowed_purchase(purchased_item_object):
                
                purchased_item_object.buy(current_user)
                
                flash(f'Purchased {purchased_item_object.name} for {purchased_item_object.price}', category='success')
            else:
                flash(f'Current budget: {current_user.budget} Item price: {purchased_item_object.price}', category='danger')
        
        #sell item logic
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.allowed_sell(sold_item_object):
                sold_item_object.sell(current_user)
                
                flash(f'Sold {sold_item_object.name} for {sold_item_object.price}', category='success')
            else:
                flash(f'Error selling. Please report Error code E1-S-{sold_item_object.owner}/{current_user.name}', category='danger')
        

        return redirect(url_for('market'))

    if request.method == "GET":
        items =  Item.query.filter_by(owner=None)
        
        owned_items = Item.query.filter_by(owner=current_user.id)

        return render_template("market.html", items=items, purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)


@app.route('/create_profile')
@login_required
def create_profile():
    if current_user.isTeacher == None:
        return render_template("create_profile.html")
    else:
        flash('You already have a profile.', 'warning')
        return redirect(url_for('job_board_page'))

@app.route('/setup_teacher_profile', methods=['GET', 'POST'])
@login_required
def setup_teacher_profile():
        
    if current_user.isTeacher == None:
        form = TeacherProfileForm()
        if form.validate_on_submit():

            # Check if the email already exists
            existing_email = TeacherProfile.query.filter_by(contact_email_address=form.contact_email_address.data).first()
            if existing_email:
                flash('Error: The email address is already in use. Please use a different email address.', category='warning')
                return redirect(url_for('setup_teacher_profile'))
        
            # Convert 'yearsOfExperience' to an integer
            years_of_experience_integer = int(form.yearsOfExperience.data)

            # Convert 'nativeEnglish' to a boolean
            native_english_boolean = form.isNativeEnglish.data == 'True'

            teacher_profile = TeacherProfile(
                id=current_user.id,
                nativeEnglish= native_english_boolean,
                yearsOfExperience=years_of_experience_integer,
                visaType=form.visaType.data,
                contact_email_address = form.contact_email_address.data,
                user=current_user
            )

            # Update isTeacher attribute for the current user
            current_user.isTeacher = True

            current_user.set_default_teacher_budget()

            db.session.add(teacher_profile)
            db.session.commit()
        
            flash(f'Teacher profile created sucessfully. You can now Quick Apply to Jobs!', category='success')
            return redirect(url_for('job_board_page'))
        
        if form.errors != {}: # If NO errors from validations (empty dict)
            for err_messages in form.errors.values():
                flash(f'Error: {err_messages}',category='danger')

        return render_template('setup_teacher_profile.html', form=form)
    else:
        flash('You already have a profile.', 'warning')
        return redirect(url_for('job_board_page'))

@app.route('/teacher_profile',methods=['GET','POST'])
@login_required
def teacher_profile():

    if current_user.isTeacher:
        teacher_profile = TeacherProfile.query.filter_by(id=current_user.id).first()
        jobs_applied = JobApplicant.query.filter_by(teacher_id = current_user.id)
        current_datetime = datetime.now()

        return render_template("teacher_profile.html", teacher_profile=teacher_profile, jobs_applied=jobs_applied, current_datetime=current_datetime)

    else:
        flash('Access denied. Only teachers can view this page.', 'warning')
        return redirect(url_for('home_page'))
    
@app.route('/setup_recruiter_profile', methods=['GET', 'POST'])
@login_required
def setup_recruiter_profile():
    if current_user.isTeacher == None:
        form = RecruiterProfileForm()
        
        if form.validate_on_submit():

             # Check if the email already exists
            existing_email = RecruiterProfile.query.filter_by(contact_email_address=form.contact_email_address.data).first()
            if existing_email:
                flash('Error: The email address is already in use. Please use a different email address.', category='warning')
                return redirect(url_for('setup_recruiter_profile'))
            
            recruiter_profile = RecruiterProfile(
                id = current_user.id,
                contact_email_address = form.contact_email_address.data
            )

            # Update isTeacher attribute for the current user, False = Recruiter
            current_user.isTeacher = False

            current_user.set_default_recruiter_budget()

            db.session.add(recruiter_profile)
            db.session.commit()
            flash(f'Recruiter profile created sucessfully. You can now post your Jobs!', category='success')
            return redirect(url_for('job_post_creation'))

        if form.errors != {}: # If NO errors from validations (empty dict)
            for err_messages in form.errors.values():
                flash(f'Error: {err_messages}',category='danger')

        return render_template('setup_recruiter_profile.html', form=form)
    else:
        flash('You already have a profile.', 'warning')
        return redirect(url_for('job_board_page'))

@app.route('/recruiter_profile',methods=['GET'])
@login_required
def recruiter_profile():

    if current_user.isTeacher == False:
        recruiter_profile = RecruiterProfile.query.filter_by(id=current_user.id).first()
        jobs_posted = JobPost.query.filter_by(recruiter_id=current_user.id).all()
        return render_template("recruiter_profile.html", recruiter_profile=recruiter_profile, jobs_posted=jobs_posted)

    else:
        flash('Access denied. Only recruiters can view this page.', 'warning')
        return redirect(url_for('home_page'))

@app.route('/job_post_creation', methods=['GET','POST'])
@login_required
def job_post_creation():
    
    # user is a recruiter
    if current_user.isTeacher == False:
        recruiter_profile = RecruiterProfile.query.filter_by(id=current_user.id).first()
        if current_user.budget < 1:
            flash(f'You ran out of Job Post tokens. Wait or get more tokens here.', category='danger')
            return redirect(url_for('job_board_page'))
        
        form = JobForm()
        if form.validate_on_submit():
            job_schedule_to_create = WorkSchedule(
                everyday_start_time=form.everyday_start_time.data,
                everyday_end_time=form.everyday_end_time.data,
                monday_start_time=form.monday_start_time.data,
                monday_end_time=form.monday_end_time.data,
                tuesday_start_time=form.tuesday_start_time.data,
                tuesday_end_time=form.tuesday_end_time.data,
                wednesday_start_time=form.wednesday_start_time.data,
                wednesday_end_time=form.wednesday_end_time.data,
                thursday_start_time=form.thursday_start_time.data,
                thursday_end_time=form.thursday_end_time.data,
                friday_start_time=form.friday_start_time.data,
                friday_end_time=form.friday_end_time.data,
                saturday_start_time=form.saturday_start_time.data,
                saturday_end_time=form.saturday_end_time.data,
                sunday_start_time=form.sunday_start_time.data,
                sunday_end_time=form.sunday_end_time.data,
                )
            db.session.add(job_schedule_to_create)
           
            # Convert String to integers
            #salary = int(form.salary.data) if form.salary.data is not None else None

            job_to_create = JobPost(
                title=form.title.data,
                location=form.location.data,
                job_type=form.job_type.data,
                location_details=form.location_details.data,
                startdate=form.startdate.data,
                asap=form.asap.data,
                kind_student=form.kind_student.data,
                elem_student=form.elem_student.data,
                midl_student=form.midl_student.data,
                high_student=form.high_student.data,
                univ_student=form.univ_student.data,
                adlt_student=form.adlt_student.data,
                health_insurance=form.health_insurance.data,
                pension=form.pension.data,
                airfare=form.airfare.data,
                severance=form.severance.data,
                housing=form.housing.data,
                housing_allowance=form.housing_allowance.data,
                vacation_days=form.vacation_days.data,
                salary=form.salary.data,
                salary_negotiable=form.salary_negotiable.data,
                salary_payment_type=form.salary_payment_type.data,
                description=form.description.data,
                recruiter_id=current_user.id,
                work_schedule=job_schedule_to_create
                )
            db.session.add(job_to_create)
            db.session.commit()
            current_user.minus_budget(1)
            flash(f'Job posted sucessfully!', category='success')
            return redirect(url_for('job_board_page'))
        
        if form.errors != {}: # If NO errors from validations (empty dict)
            for err_messages in form.errors.values():
                flash(f'Error: {err_messages}',category='danger')

        return render_template('job_post_creation.html', form=form, recruiter_profile=recruiter_profile)
    
    else:
        flash('Access denied. Only Recruiters can view this page.', 'warning')
        return redirect(url_for('home_page'))


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email_address = form.email_address.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create) #login the user, when user created success
        flash(f'Account created sucessfully. You are logged-in as {user_to_create.username}.', category='success')
        return redirect(url_for('create_profile'))
    
    if form.errors:
        for field_errors in form.errors.values():
            err_message = ', '.join(field_errors)
            if 'Field must be equal to password1.' in err_message:
                flash('Passwords do not match', category='warning')
            else:
                flash(err_message, category='warning')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user =  User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Logged in as {attempted_user.username}', category='info')
            return redirect(url_for('job_board_page'))
        else:
            flash(f'Wrong Username or Password',category='warning')
    
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have logged out', category='info')
    return redirect(url_for("home_page"))
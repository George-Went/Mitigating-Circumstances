

# Flask Imports 
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Flask-Login Imports
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

# Flask-WTF Imports 
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, ValidationError, DataRequired, Email, EqualTo

#Flask-Dance Imports
from flask_dance.contrib.google import make_google_blueprint, google

# Configuration imports 
from config import Config

#google cloud imports
import logging
import os


#from models import User
from forms import *
from controllers import *
from models import *

#Models for the noSQL database 

app = Flask(__name__)
app.config.from_object(Config)


csrf = CSRFProtect(app) #csrf token used with flaskWTF forms


# --------------------------------------------
# GENERATING TEST DATA 
# --------------------------------------------

@app.route('/generatedata')
def generatedata():

    # Creating test users
    UserController().create(
        name = "George",
        email = "gep.went@gmail.com",
        password = generate_password_hash("password"),
    )

    UserController().create(
        name = "Mark",
        email = "mark@gmail.com",
        password = generate_password_hash("password"),
    )

    UserController().create(
        name = "Dave",
        email = "dave@gmail.com",
        password = generate_password_hash("password"),
    )

    # Setting a user as a staff member 
    StaffController().create(
        name = "Dave",
        email = "dave@gmail.com",
    )

    # Creating example subjects
    SubjectController().create(
        name = "History"
    )

    SubjectController().create(
        name = "Maths"
    )

    # Creating test mitigating circumstances submissions 
    MitigatingCircumstanceController().create(
        student = "Mark",
        student_email = "mark@gmail.com",
        subject = "Data Mining",
        title = "Working out Nearest Neigbour",
        reason = "Hi sir, im having issues with working out how nearest neighbour works, please advise",
        state = "New"
    )

    MitigatingCircumstanceController().create(
        student = "John",
        student_email = "john@btinternet.com",
        subject = "Networks",
        title = "Ping system",
        reason = "How do i ping a server",
        state = "Under Review"
    )


    flash('data added')
    return redirect('/')



## ---------------------------------------
## LOGIN SYSTEM
## ---------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#if a user is unauthorized or is not logged in, goes to /login


#login use reloads an object when a user loads a new page 
@login_manager.user_loader 
def load_user(email):
    return User.query().filter(User.email==email).get()

@app.route('/')
def index():
    return redirect(url_for('login'))

## LOGIN PAGE --------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit(): ## if the form is submitted with the correct data       
        check = form.email.data
        #get User data based on the email address entered
        user = User.query(User.email == check).get()
        if user:

           # if user.password == form.password.data:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect(url_for('dashboard'))
        
        return "<h1>Invalid username or password</h1>"
    else:
        return render_template('login/login.html', form = form)
    return render_template('login/login.html', form = form)

# Logout function
@app.route('/logout')
@login_required
def logout():
    logout_user()
    print "you are now logged out"
    return redirect(url_for('login'))

#check user
@app.route('/user')
@login_required
def checkuser():

    print "the user is: " + current_user.name
    return "The current user is: " + current_user.name + " " + current_user.email



## ---------------------------------------
## CREATE USER SYSTEM
## ---------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():  
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        UserController().create(
            name = name,
            email = email,
            password = password
        )

        if form.staff.data:
            StaffController().create(
                name = name,
                email = email
            )
            print "STAFF: YES"
            flash ("Staff account: " + str(email) + " created") 
        else:
            print "STAFF: NO"
            flash ("Student account: " + str(email) + " created") 


        print "NAME: " + str(request.form['name'])
        print "EMAIL: " + str(request.form['email'])
        print "PASSWORD: " + str(request.form['password'])

        hashed_password = generate_password_hash(request.form['password'])
        print "HASHED PASSWORD: " + hashed_password

     

        end_result = check_password_hash(hashed_password, request.form['password'])

        print "PASSWORDS MATCH: " + str(end_result)
        return redirect('/login')

    return render_template('login/signup.html')


## ---------------------------------------
## STUDENTS SYSTEM 
## --------------------------------------- 

## STUDENT DASHBOARD ---------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    admincheck = StaffModel.query(StaffModel.email == current_user.email).get()
    if admincheck:
        return redirect ('/admindashboard')
    else:
        queryemail = MitigatingCircumstanceController().querybyemail(current_user.email)



        
        return render_template(
        '/dashboard.html',
        title='Example Form Index',
        MitigatingCircumstances = queryemail
        )  



## SUBMITTING MITIGATING CIRCUMSTANCES -----------------------------------


@app.route('/submit_mitcert', methods=['GET','POST'])
def submitMitigatingCircumstance():
    form = MitigatingCircumstanceForm()

    query_subjects  = SubjectController().index()

    if request.method == 'POST' :
        MitigatingCircumstanceController().create(
            student = current_user.name,
            student_email = current_user.email,
            subject = request.form['subject'],
            title = request.form['title'],
            reason = request.form['reason'],
            state = "New"
        )
        flash('mitigating circumstance submitted')
        return redirect (url_for('dashboard'))
        
    return render_template(
                        'mitcert/create.html', 
                        title='Mitigating circumstance Form', 
                        form=form,
                        Subjects=query_subjects
                        )

## EDITING MITIGATING CIRCUMSTANCES ----------------------------------

@app.route('/<id>/edit', methods=['GET','POST'])
def editMitigatingCircumstance(id): #this variable is taken from the url 
    form = MitigatingCircumstanceForm()

    queryid = int(id)# converts the html id into a int
    query_mitcert = MitigatingCircumstanceController().querybyid(queryid)
    query_subjects = SubjectController().index()

    if request.method == 'POST' and form.validate_on_submit():#does it have a post method

        MitigatingCircumstanceController().edit(
            id = queryid,
            student = current_user.name,
            student_email = current_user.email,
            subject = request.form['subject'],
            title = request.form['title'],
            reason = request.form['reason'],
            state = query_mitcert.state
        )
        flash('mitigating circumstance updated')
        return redirect('/dashboard')
  
  
    return render_template(
        'mitcert/edit.html',
         title ='form show', 
         form = form,
         data = query_mitcert,
         Subjects = query_subjects
         )



## ---------------------------------------
## STAFF SYSTEM
## ---------------------------------------

## ADMIN DASHBOARD ------------------------------------------------
@app.route('/admindashboard')
@login_required
def admindashboard():
    
    admincheck = StaffModel.query(StaffModel.email == current_user.email).get()
    if admincheck:
        query = MitigatingCircumstanceController().index()
    
        return render_template(
            '/admindashboard.html',
            title='Example Form Index',
            MitigatingCircumstances = query
        )  

    else:
        flash('you are not a staff memeber')
        return redirect ('/dashboard')

    
## ADDING / REMOVING SUBJECTS ------------------------------------
@app.route('/subjects', methods=['GET','POST'])
@login_required
def subjects():
    form = AddsubjectsForm()
    query_subjects = SubjectController().index()


    if request.method == 'POST':

        SubjectController().create(
            name = request.form['subject']
        )
        
        print "NEW SUBJECT: " + str(request.form['subject'])
        
        #return redirect ('/subjects')
        return render_template(
            '/mitcert/subjects.html',
            title='Example Form Index',
            Subjects = query_subjects, 
            form = form
            )
        
    return render_template(
        '/mitcert/subjects.html',
        title='Example Form Index',
        Subjects = query_subjects, 
        form = form
    ) 

## REVIEWING MITIGATING CIRCUMSTANCES

@app.route('/<id>/review', methods=['GET','POST'])
def reviewMitigatingCircumstance(id):
    
    admincheck = StaffModel.query(StaffModel.email == current_user.email).get()
    if admincheck:

        form = MitigatingCircumstanceForm()

        queryid = int(id)# converts the html id into a int
        query_mitcert = MitigatingCircumstanceController().querybyid(queryid)

        if request.method == 'POST' :#does it have a post method
            
            

            print "STATE: " + request.form['state']

            MitigatingCircumstanceController().edit(
                id = id,
                student = query_mitcert.student,
                student_email = query_mitcert.student_email,
                subject = query_mitcert.subject,
                title = query_mitcert.title,
                reason = query_mitcert.reason,
                state = request.form['state']
            )
            flash('mitigating circumstance updated')
            return redirect('/dashboard')
    
    
        return render_template(
            'mitcert/review.html',
            title ='form show', 
            form = form,
            MitigatingCircumstance = query_mitcert
            )

    else:
        flash('you are not a staff memeber')
        return redirect ('/dashboard')




## ---------------------------------------
## ERROR HANDELING
## ---------------------------------------
    
@app.errorhandler(404)
def erro404(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404    

@app.errorhandler(500)
def error500(e):
    # note that we set the 404 status explicitly
    return render_template('errors/500.html'), 500    


























## ---------------------------------------
## EXAMPLE CRUD APP
## ---------------------------------------

#index of datasets
@app.route('/examplecrud/index', methods=['GET'])
def exampleFormGet():
    
    return render_template(
        'examplecrud/index.html',
        title='Example Form Index',
        data=ExampleDataController().index()
    )              


# Creating a dataset
@app.route('/examplecrud/create', methods=['GET','POST'])
def exampleFormCreate():
    form = ExampleDataForm()
    if request.method == 'POST' and form.validate_on_submit():

        ExampleDataController().create(
            name = request.form['name'],
            text = request.form['text']
        )

        print request.form['name']
        print request.form['text']

        return redirect('examplecrud/create')
    return render_template(
                        'examplecrud/create.html', 
                        title='Example Form', 
                        form=form
                        )




@app.route('/<id>/edit', methods=['GET','POST'])
def editForm(id): #this variable is taken from the url 
    form = ExampleDataForm()

    queryid = int(id)# converts the html id into a int
    if request.method == 'POST' and form.validate_on_submit():#does it have a post method

        ExampleDataController().edit(
            id = queryid,
            name = request.form['name'],
            text = request.form['text']
        )
        return redirect('/'+id+'/edit')
  
  
    return render_template(
        'examplecrud/edit.html',
         title ='form show', 
         form = form,
         data = ExampleDataController().query(queryid) ##used to query the correct data to display
         )



@app.route('/<id>/delete', methods=['GET','POST'])
def deleteForm(id):
    queryid = int(id)
    #if request.method == 'POST':
    ExampleDataController().delete(id = queryid)
    print "delet"

    return redirect('examplecrud/index')
    


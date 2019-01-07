#Models for the noSQL database 
from google.appengine.ext import ndb
from flask_login import UserMixin


# User Model 
# Used as part of the flask-login addon
# Is called by the @login_manager and @Login Required functions 
# is also stored in the ndb database as User 

class User(UserMixin, ndb.Model): #google noSQL model creation   
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class SubjectModel(ndb.Model):
    name = ndb.StringProperty()

class StaffModel(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()


class MitigatingCircumstanceModel(ndb.Model): #google noSQL model creation   
    student = ndb.StringProperty()
    student_email = ndb.StringProperty()
    subject = ndb.StringProperty()
    title = ndb.StringProperty()
    reason = ndb.TextProperty()
    state = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)

# Example data model
# Is used in the Example CRUD applicaion 
class ExampleDataModel(ndb.Model):
    name = ndb.StringProperty()
    text = ndb.StringProperty()

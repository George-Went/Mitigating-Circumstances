

from flask_login import LoginManager, current_user, login_user

from google.appengine.ext import ndb
import os
import cloudstorage as gcs

from google.appengine.api import app_identity 

from models import *



# User 
class UserController():
    def create (self,name,email,password):
		user = User()
		user.name = name
		user.email = email
		user.password = password
		user.put()
		return user

class StaffController():
	def create (self,name,email):
		staff = StaffModel()
		staff.name = name
		staff.email = email
		staff.put()
		return staff
	
class SubjectController():
	def create (self,name):
		subject = SubjectModel()
		subject.name = name
		subject.put()
		return subject
	
	def index(self):	
		return SubjectModel.query().fetch() 

##--------------------------------------------------------------
## MITIGATING CIRCUMSTACES CONTROLLER
## Used as  a controller for the MitigatingCircumstances Model 
##--------------------------------------------------------------

class MitigatingCircumstanceController():
	def create (self, student, student_email, subject, title, reason, state):
		mitigatingCircumstance = MitigatingCircumstanceModel()
		mitigatingCircumstance.student = student
		mitigatingCircumstance.student_email = student_email
		mitigatingCircumstance.subject = subject
		mitigatingCircumstance.title = title
		mitigatingCircumstance.reason = reason
		mitigatingCircumstance.state = state
		mitigatingCircumstance.put() 
		return mitigatingCircumstance

	def edit (self, id, student, student_email, subject, title, reason, state):
		mitigatingCircumstance = MitigatingCircumstanceModel.get_by_id(int(id)) #the dataset is slected based on its id
		mitigatingCircumstance.student = student
		mitigatingCircumstance.student_email = student_email
		mitigatingCircumstance.subject = subject
		mitigatingCircumstance.title = title
		mitigatingCircumstance.reason = reason
		mitigatingCircumstance.state = state
		mitigatingCircumstance.put() 
		return mitigatingCircumstance

	def delete(self,id):
		exampleData = ExampleDataModel.get_by_id(int(id))
		return exampleData.key.delete()
	
	def index(self):	
		return MitigatingCircumstanceModel.query().fetch() 

	def querybyemail(self, email):
		query = MitigatingCircumstanceModel.query(MitigatingCircumstanceModel.student_email == email).fetch()   
		return query

	def querybyid(self, id):
		return MitigatingCircumstanceModel.get_by_id(int(id))


## -------------------------
## EXAMPLE DATA CONTROLLER
## Used as a controller for the Example Data Controller CRUD App 
## -------------------------

class ExampleDataController():
	def create (self,name,text):
	#creates students
	#assignes the variables to the model
		exampleData = ExampleDataModel() #speuserusercifies the creation of a new dataset
		exampleData.name = name #links the data to the importted vars
		exampleData.text = text
		exampleData.put() # 'puts' the data into the noSQL storage and generates a key 
		return exampleData

	def edit (self,id,name,text):
		exampleData = ExampleDataModel.get_by_id(int(id)) #the dataset is slected based on its id
		exampleData.name = name 
		exampleData.text = text
		exampleData.put()
		return exampleData


	def delete(self,id):
		exampleData = ExampleDataModel.get_by_id(int(id))
		return exampleData.key.delete()


	def index(self):	
		return ExampleDataModel.query().fetch() # returns all of type exampledatamodel

	def query(self, id):
		return ExampleDataModel.get_by_id(int(id))
		# for queries you can also use ExampleDataModel.query(ExampleDate.name == "obi wa")


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, FileField
from wtforms.validators import InputRequired, ValidationError, DataRequired, Email, EqualTo





## Login Form - used when a user is logging into an exisiting account
class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember Me')

## Registration Form - Used when a user is creating a new account
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    name = StringField('username', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])
    staff = BooleanField('staff')

## Mitigating Circumstances Form
class MitigatingCircumstanceForm(FlaskForm):
    title = StringField('title', validators=[InputRequired()])
    subject = StringField('subject', validators=[InputRequired()])
    reason = StringField('reason', validators=[InputRequired()])



## Adding a subject form
class AddsubjectsForm(FlaskForm):
    subject = StringField('subject', validators=[InputRequired()])


## Example Data Form
class ExampleDataForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('name')
    text = StringField('text')
    submit = SubmitField('create')

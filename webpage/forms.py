from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from webpage.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

images = UploadSet('images', IMAGES)
state_addbrev = [ ('NA','None'), ('NA','Indian' )]

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class add_details(FlaskForm):
    Fullname = StringField('Full_name (as per ID proof)',
                        validators=[DataRequired(), Length(min=2, max=20)])
    state = SelectField(label='Nationality', choices=state_addbrev)
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])

    submit = SubmitField('submit')


    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class drone_details(FlaskForm):
    Dronename = StringField('Dronename',
                        validators=[DataRequired(), Length(min=2, max=20)])
    nameOfManufacture = StringField('nameOfManufacture',
                        validators=[DataRequired(), Length(min=2, max=20)])
    droneType = StringField('droneType',
                        validators=[DataRequired(), Length(min=2, max=20)])
    maxTakeOffWeight = StringField('maxTakeOffWeight',
                        validators=[DataRequired(), Length(min=2, max=20)])
    maxHeightAttainable = StringField('maxHeightAttainable',
                        validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('submit')

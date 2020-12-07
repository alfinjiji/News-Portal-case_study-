from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
from flask_login import current_user
from news_portal.models import User

# Registration form validation
class RegistrationForm(FlaskForm):
    fname = StringField('fname', validators=[DataRequired(), Length(min=3, max=10)])
    lname = StringField('lname', validators=[DataRequired(), Length(min=1)])
    mobile = IntegerField('mobile', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', widget=TextArea(), validators=[DataRequired()]) # for textarea
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SIGN UP') # Sign Up will shown in button

    # custom validation for check if enter same email that already register
    """
    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')
    """
    """
    # validate username. check the username already register or not
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # if user exist validation error will raise
        if user:
            raise ValidationError('That username is taken. Please Choose a different one.')
    """

    # validate Email. check the email already register or not
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if user exist validation error will raise
        if user:
            raise ValidationError('That Email is taken. Please Choose a different one.')
    
# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LOGIN')

# Profile update form
class UserUpdate(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=5, max=20)])
    mobile = IntegerField('mobile', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', widget=TextArea(), validators=[DataRequired()]) 
    image = FileField('Update profile pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPDATE') # Sign Up will shown in button
    # validate Email. check the email already register or not
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # if user exist validation error will raise
            if user:
                raise ValidationError('That Email is taken. Please Choose a different one.')

# Feedback form
class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = StringField('Message', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('SUBMIT NOW')

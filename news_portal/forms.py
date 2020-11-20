from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
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
    
# add news form
class NewsForm(FlaskForm):
    heading = StringField('News Heading', validators=[DataRequired()])
    description = StringField('News Description', widget=TextArea(), validators=[DataRequired()])
    district = SelectField(u'District', choices=[("",'-- choose district --'),
                        ('Kasaragod','Kasaragod'), ('Kannur','Kannur'), 
                        ('Wayanad','Wayanad'), ('Kozhikode','Kozhikode'),
                        ('Malappuram','Malappuram'), ('Palakkad','Palakkad'),
                        ('Thrissur','Thrissur'), ('Ernakulam','Ernakulam'), 
                        ('Idukki','Idukki'), ('Kottayam','Kottayam'), 
                        ('Alappuzha','Alappuzha'), ('Pathanamthitta','Pathanamthitta'), 
                        ('Kollam','Kollam'), ('Thiruvananthapuram','Thiruvananthapuram')], validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    category = SelectField('News Category', choices=[("",'-- choose category --'),('Busness','Busness'),
                    ('Entertainment','Entertainment'),('Politics','Politics'),
                    ('Sports','Sports'),('Technology','Technology'),('Travel','Travel')], validators=[DataRequired()])
    news_img = FileField('News Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('ADD NEWS')

# edit news form
class EditNewsForm(FlaskForm):
    heading = StringField('News Heading', validators=[DataRequired()])
    description = StringField('News Description', widget=TextArea(), validators=[DataRequired()])
    district = SelectField(u'District', choices=[("",'-- choose district --'),('kannur','Kannur'),('calicut','calicut')], validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    category = SelectField('News Category', choices=[("",'-- choose category --'),('Busness','Busness'),('Entertainment','Entertainment'),('International','International'),('Politics','Politics'),('Sports','Sports'),('Technology','Technology'),('Travel','Travel')], validators=[DataRequired()])
    news_img = FileField('News Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPDATE NEWS')

    


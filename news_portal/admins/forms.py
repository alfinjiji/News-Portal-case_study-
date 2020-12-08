from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, SelectField,  SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from wtforms.widgets import TextArea
from news_portal.models import User

# Admin Login form
class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN IN')

# Admin create user form
class CreateUserForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired(), Length(min=3, max=10)])
    lname = StringField('Last name', validators=[DataRequired(), Length(min=1)])
    mobile = IntegerField('Mobile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', widget=TextArea(), validators=[DataRequired()]) # for textarea
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    userole = SelectField('User Type', choices=[("",'-- choose account type --'), ('user','user'), ('admin','admin')], validators=[DataRequired()])
    submit = SubmitField('Register Now')

    # validate Email. check the email already register or not
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if user exist validation error will raise
        if user:
            raise ValidationError('That Email is taken. Please Choose a different one.')

# Admin User Update
class AdminUserUpdate(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=5, max=20)])
    mobile = IntegerField('mobile', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', widget=TextArea(), validators=[DataRequired()]) 
    userole = SelectField('User Type', choices=[("",'-- choose account type --'), ('user','user'), ('admin','admin')], validators=[DataRequired()])
    submit = SubmitField('Update User') 

# Admin Upload News form
class AdminNewsForm(FlaskForm):
    heading = StringField('News Heading', validators=[DataRequired()])
    description = StringField('News Description', widget=TextArea(), validators=[DataRequired()])
    district = SelectField('District', choices=[("",'-- choose district --'),
                        ('Kasaragod','Kasaragod'), ('Kannur','Kannur'), 
                        ('Wayanad','Wayanad'), ('Kozhikode','Kozhikode'),
                        ('Malappuram','Malappuram'), ('Palakkad','Palakkad'),
                        ('Thrissur','Thrissur'), ('Ernakulam','Ernakulam'), 
                        ('Idukki','Idukki'), ('Kottayam','Kottayam'), 
                        ('Alappuzha','Alappuzha'), ('Pathanamthitta','Pathanamthitta'), 
                        ('Kollam','Kollam'), ('Thiruvananthapuram','Thiruvananthapuram')], validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    category = SelectField('News Category', choices=[("",'-- choose category --'),('Business','Business'),
                    ('Entertainment','Entertainment'),('Politics','Politics'),
                    ('Sports','Sports'),('Technology','Technology'),('Travel','Travel')], validators=[DataRequired()])
    img = FileField('News Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload Now')

# Admin Update News form
class AdminNewsUpdate(FlaskForm):
    heading = StringField('News Heading', validators=[DataRequired()])
    description = StringField('News Description', widget=TextArea(), validators=[DataRequired()])
    district = SelectField('District', choices=[("",'-- choose district --'),
                        ('Kasaragod','Kasaragod'), ('Kannur','Kannur'), 
                        ('Wayanad','Wayanad'), ('Kozhikode','Kozhikode'),
                        ('Malappuram','Malappuram'), ('Palakkad','Palakkad'),
                        ('Thrissur','Thrissur'), ('Ernakulam','Ernakulam'), 
                        ('Idukki','Idukki'), ('Kottayam','Kottayam'), 
                        ('Alappuzha','Alappuzha'), ('Pathanamthitta','Pathanamthitta'), 
                        ('Kollam','Kollam'), ('Thiruvananthapuram','Thiruvananthapuram')], validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    category = SelectField('News Category', choices=[("",'-- choose category --'),('Business','Business'),
                    ('Entertainment','Entertainment'),('Politics','Politics'),
                    ('Sports','Sports'),('Technology','Technology'),('Travel','Travel')], validators=[DataRequired()])
    img = FileField('News Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update News')
    
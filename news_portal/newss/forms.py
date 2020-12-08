from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import TextArea

# add news form
class NewsForm(FlaskForm):
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
    news_img = FileField('News Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('ADD NEWS')

# edit news form
class EditNewsForm(FlaskForm):
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
    news_img = FileField('News Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPDATE NEWS')

    
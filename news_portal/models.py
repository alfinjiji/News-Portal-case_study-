import os
import os.path as op
# model.py is for creating Models or tables
from datetime import datetime
from news_portal import db, login_manager, ad, file_path
from flask_login import UserMixin
# flask-admin
from flask_admin import form
from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

# function for get an user by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='user.jpg')
    password = db.Column(db.String(100), nullable=False)  
    news = db.relationship('News', backref='user', lazy=True)                 

    def  __repr__(self):
        return f"User %r('{self.name}', '{self.mobile}' '{self.email}', '{self.address}')" % self.id

# News Model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    district = db.Column(db.String(20), nullable=False)
    place = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    news_img = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Boolean)

    def  __repr__(self):
        return f"News('{self.heading}', '{self.description}', '{self.district}', '{self.place}', '{self.category}', '{self.news_img}', '{self.date}')"

# Flask Admin
class FileView(sqla.ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'news_img': form.FileUploadField
    }
    # Pass additional parameters to 'news_img' to FileUploadField constructor
    form_args = {
        'news_img': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }
    # Override form field to use Flask-Admin form_choice
    form_choices = {
        'district': [ 
                        ("",'-- choose district --'),
                        ('Kasaragod','Kasaragod'), ('Kannur','Kannur'), 
                        ('Wayanad','Wayanad'), ('Kozhikode','Kozhikode'),
                        ('Malappuram','Malappuram'), ('Palakkad','Palakkad'),
                        ('Thrissur','Thrissur'), ('Ernakulam','Ernakulam'), 
                        ('Idukki','Idukki'), ('Kottayam','Kottayam'), 
                        ('Alappuzha','Alappuzha'), ('Pathanamthitta','Pathanamthitta'), 
                        ('Kollam','Kollam'), ('Thiruvananthapuram','Thiruvananthapuram')
                    ],
        'category': [ 
                        ("",'-- choose category --'),
                        ('Busness','Busness'), ('Entertainment','Entertainment'),
                        ('International','International'), ('Politics','Politics'),
                        ('Sports','Sports'), ('Technology','Technology'), ('Travel','Travel')
                    ]
    }

ad.add_view(ModelView(User, db.session))    
ad.add_view(FileView(News, db.session))
path = op.join(op.dirname(__file__), 'static/upload_pic')
ad.add_view(FileAdmin(path, '/static/upload_pic', name='Static Files'))


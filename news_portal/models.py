import os
import os.path as op
# model.py is for creating Models or tables
from datetime import datetime
from news_portal import db #, login_manager #, file_path, ad
from news_portal.users import login_manager
from flask_login import UserMixin, current_user

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
    userole = db.Column(db.String(20), nullable=False, default='user')  

    def isAdmin(self):
        if self.userole == 'admin':
            return True
        else:
            return False

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
    status = db.Column(db.String(20), nullable=False, default='pending')

    def  __repr__(self):
        return f"News('{self.heading}', '{self.description}', '{self.district}', '{self.place}', '{self.category}', '{self.news_img}', '{self.date}')"

# User Feedback
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def  __repr__(self):
        return f"User %r('{self.name}', '{self.email}' '{self.message}')" % self.id

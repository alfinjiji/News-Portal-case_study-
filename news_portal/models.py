# model.py is for creating Models or tables
from datetime import datetime
from news_portal import db, login_manager 
from flask_login import UserMixin

# function for get an user by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)                   

    def  __repr__(self):
        return f"User %r('{self.name}', '{self.mobile}' '{self.email}', '{self.address}')" % self.id

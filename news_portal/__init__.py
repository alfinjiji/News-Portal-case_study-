import os
import os.path as op
# initializing the application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # for hashed password
#from flask_login import LoginManager # for login functions
#flask-Admin module
from flask_admin import Admin
 
app = Flask(__name__)
# protect from modify cookies
app.config['SECRET_KEY'] = '825515e35cea3279818d369c35b72a70'
#configuration for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static/upload_pic')
try:
    os.mkdir(file_path)
except OSError:
    pass

# database object
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)
#login_manager.login_view = 'users.login' 
#login_manager.login_message_category = 'info'

from news_portal.users.routes import users
from news_portal.newss.routes import newss
from news_portal.main.routes import main
from news_portal.admins.routes import admin

app.register_blueprint(users)
app.register_blueprint(newss)
app.register_blueprint(main)
app.register_blueprint(admin, url_prefix="/admin")

#from news_portal import admin_dashboard
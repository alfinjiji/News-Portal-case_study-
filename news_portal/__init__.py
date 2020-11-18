import os
import os.path as op
# initializing the application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # for hashed password
from flask_login import LoginManager # for login functions
#flask-Admin module
from flask_admin import Admin
 
app = Flask(__name__)
# protect from modify cookies
app.config['SECRET_KEY'] = '825515e35cea3279818d369c35b72a70'
#configuration for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#admin
app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
ad = Admin(app, name='Admin', template_mode='bootstrap3')
# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static/upload_pic')
try:
    os.mkdir(file_path)
except OSError:
    pass

# database object
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# for login_required
# if we try to access account page it will redirect to login page
login_manager.login_view = 'login' # login is our function name of route
login_manager.login_message_category = 'info' # nicly coloured blue alert

from news_portal import routes # import all routes that we created

"""
from news_portal.admin.routes import admin
app.register_blueprint(admin, url_prefix="/admin")
"""
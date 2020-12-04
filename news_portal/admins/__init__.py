import os
import os.path as op
from flask import Blueprint
from flask_login import LoginManager
from flask_admin import Admin
from news_portal import app

admin = Blueprint('admins', __name__)
app.config['FLASK_ADMIN_SWATCH'] = 'slate'
ad = Admin(app, name='Admin', template_mode='bootstrap3')
login_manager = LoginManager(app)
login_manager.login_view = 'admins.login' 
login_manager.login_message_category = 'info'
# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static/upload_pic')
try:
    os.mkdir(file_path)
except OSError:
    pass
 
from news_portal.admins import routes
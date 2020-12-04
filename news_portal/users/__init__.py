from news_portal import app
from flask_login import LoginManager

login_manager = LoginManager(app)
login_manager.login_view = 'users.login' 
login_manager.login_message_category = 'info'
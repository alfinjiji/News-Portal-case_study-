import os
import os.path as op
from flask_login import current_user
from flask_admin import form, Admin
from flask_admin.contrib import sqla, rediscli
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from news_portal import app, db
from news_portal.models import User, News
from sqlalchemy.event import listens_for

app.config['FLASK_ADMIN_SWATCH'] = 'slate'
ad = Admin(app, name='Admin', template_mode='bootstrap3')
# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static/upload_pic')
try:
    os.mkdir(file_path)
except OSError:
    pass
 

# Delete hooks for models, delete files if models are getting deleted
@listens_for(News, 'after_delete')
def del_file(mapper, connection, target):
    if target.news_img:
        try:
            os.remove(op.join(file_path, target.news_img))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

class FileView(sqla.ModelView):
    """
    def is_accessible(self):
        return current_user.is_authenticated
    """
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

class MyModelView(ModelView):
    form_excluded_columns = ['news']
    form_choices = {
        'userole': [
            ("user", "user"),
            ("admin", "admin")
        ]}
    form_args = {
        'userole': {
            'label': 'User_Type'
        }
    }
    """
    def is_accessible(self):
            return current_user.is_authenticated
            """
"""
class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated
"""
ad.add_view(MyModelView(User, db.session))    
ad.add_view(FileView(News, db.session))

# path = op.join(op.dirname(__file__), 'static/upload_pic')
# ad.add_view(MyFileAdmin(path, '/static/upload_pic', name='Static Files'))



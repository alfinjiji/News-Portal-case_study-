import os
import os.path as op
from news_portal.models import User, News
from news_portal.admins import admin, file_path
from news_portal.admins.models import Admins
from sqlalchemy.event import listens_for

# Delete hooks for models, delete files if models are getting deleted
@listens_for(News, 'after_delete')
def del_file(mapper, connection, target):
    if target.news_img:
        try:
            os.remove(op.join(file_path, target.news_img))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

@admin.route('/admin-login')
def adminLogin():
    admins = Admins.query.get(1)
    login_user(admins)
    return "admin Logged in"


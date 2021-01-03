import os
import os.path as op
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from news_portal import db, bcrypt, app
from news_portal.models import User, News, Feedback
from news_portal.admins.forms import AdminLoginForm, CreateUserForm, AdminUserUpdate, AdminNewsForm, AdminNewsUpdate
from news_portal.main.utils import save_image
from news_portal.users.forms import UserUpdate

admin = Blueprint('admins', __name__)

# Admin login 
@admin.route('admin-login', methods=['GET', 'POST'])
@admin.route('/', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            return redirect(url_for('admins.admin_home'))
    form = AdminLoginForm()
    if form.validate_on_submit():  
        user = User.query.filter_by(email=form.email.data, userole='admin').first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('admins.admin_home'))
        else:
            flash('Login Unsuccessfull. Please check username and password', 'danger')
    return render_template('admin_login.html', title="login", form=form)

# Admin Logout
@admin.route('/admin_logout')
def admin_logout():
     logout_user()
     return redirect(url_for('admins.admin_login'))

# Admin dashboard
@admin.route('admin-home')
def admin_home():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            return render_template('admin_home.html', title="home")
    return redirect(url_for('admins.admin_login'))

# Admin Profile
@admin.route('admin-profile', methods=['GET', 'POST'])
def admin_profile():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            form = UserUpdate()
            if form.validate_on_submit():
                if form.image.data:
                    try:
                        if current_user.image != "user.jpg":
                            os.unlink(os.path.join(app.root_path, 'static/upload_pic', current_user.image))
                        img_file = save_image(form.image.data)
                        current_user.image = img_file
                    except:
                        img_file = save_image(form.image.data)
                        current_user.image = img_file
                current_user.name = form.name.data
                current_user.email = form.email.data
                current_user.mobile = form.mobile.data
                current_user.address = form.address.data
                db.session.commit()
                flash('Your Account has been updated!','success')
                return redirect(url_for('admins.admin_profile'))
            elif request.method == 'GET':
                form.name.data = current_user.name
                form.email.data = current_user.email
                form.mobile.data = current_user.mobile
                form.address.data = current_user.address
            image = url_for('static', filename='upload_pic/'+current_user.image)
            return render_template('admin_profile.html', title="Profile", form=form, image=image)
    return redirect(url_for('admins.admin_login'))

# Admin Change Password
@admin.route('admin-change_password', methods=['POST'])
def admin_change_password():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            if request.method == 'POST':
                if bcrypt.check_password_hash(current_user.password, request.form['current_password']):
                    if request.form['new_password'] == request.form['confirm_password']:
                        new_password = bcrypt.generate_password_hash(request.form['new_password']).decode('utf-8')
                        current_user.password = new_password
                        db.session.commit()
                        flash('Your Password has been changed successfully! Please Login!','success')
                        return redirect(url_for('admins.admin_logout'))
                else:
                    flash('Current password mismatch, Please try again', 'danger')
            return redirect(url_for('admins.admin_profile'))
    return redirect(url_for('admins.admin_login'))

# Admin User view and Add user
@admin.route('admin-user', methods=['GET', 'POST'])
def admin_user():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            form = CreateUserForm()
            user = User.query.all()
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                fullname = form.fname.data +" "+form.lname.data
                user = User(name=fullname, mobile=form.mobile.data, email=form.email.data, address=form.address.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash('User account has been created!', 'createuser')
                return redirect(url_for('admins.admin_user'))
            return render_template('admin_user.html', title="user", user=user, form=form)
    return redirect(url_for('admins.admin_login'))

# Admin Edit User
@admin.route('/edituser/<int:user_id>', methods=['GET', 'POST'])
def edituser(user_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            form = AdminUserUpdate()
            user = User.query.filter_by(id=user_id).first()
            if form.validate_on_submit():
                try:
                    user.name = form.name.data
                    user.email = form.email.data
                    user.mobile = form.mobile.data
                    user.address = form.address.data
                    user.userole = form.userole.data
                    db.session.commit()
                    flash('user account has been updated!','success')
                    return redirect(url_for('admins.admin_user'))
                except:
                    flash('Email already exist!','danger')
                    return redirect(url_for('admins.edituser', user_id=user_id))
            elif request.method == 'GET':
                form.name.data = user.name
                form.email.data = user.email
                form.mobile.data = user.mobile
                form.address.data = user.address
                form.userole.data = user.userole
            return render_template('admin_edit_user.html', form=form)
    return redirect(url_for('admins.admin_login'))

# Delete User
@admin.route('/deleteuser/<int:user_id>', methods=['POST'])
def deleteuser(user_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            usr = User.query.get_or_404(user_id)
            db.session.delete(usr)
            db.session.commit()
            flash('User has been deleted!', 'success')
            return redirect(url_for('admins.admin_user'))
    return redirect(url_for('admins.admin_login'))

# Admin News View and Add News
@admin.route('admin-news', methods=['GET', 'POST'])
def admin_news():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            form = AdminNewsForm()
            news = News.query.order_by(News.date.desc()).all()
            if form.validate_on_submit():
                if form.img.data:
                    img_file = save_image(form.img.data)
                    img = img_file
                news = News(heading=form.heading.data, description=form.description.data, district=form.district.data, place=form.place.data, category=form.category.data, news_img=img, status=form.status.data, uid=current_user.id)
                db.session.add(news)
                db.session.commit()
                flash('News Uploaded Successfully!', 'uploadnews')
                return redirect(url_for('admins.admin_news'))
            return render_template('admin_news.html', title="news", news=news, form=form)
    return redirect(url_for('admins.admin_login'))

# Admin Edit News
@admin.route('/editnews/<int:news_id>', methods=['GET', 'POST'])
def editnews(news_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            form = AdminNewsUpdate()
            current_news = News.query.filter_by(id=news_id).first()
            if form.validate_on_submit():
                if form.img.data:
                    try:
                        os.unlink(os.path.join(app.root_path, 'static/upload_pic', current_news.news_img))
                        img_file = save_image(form.img.data)
                        current_news.news_img = img_file
                    except:
                        img_file = save_image(form.img.data)
                        current_news.news_img = img_file
                current_news.heading = form.heading.data
                current_news.description = form.description.data
                current_news.district = form.district.data
                current_news.place = form.place.data
                current_news.category = form.category.data
                current_news.status = form.status.data
                db.session.commit()
                flash('News has been updated!','success')
                return redirect(url_for('admins.admin_news', news_id=current_news.id))
            elif request.method == 'GET':
                form.heading.data = current_news.heading
                form.description.data = current_news.description
                form.district.data = current_news.district
                form.place.data = current_news.place
                form.category.data = current_news.category
                form.status.data = current_news.status
            return render_template('admin_edit_news.html', title="Edit_news", form=form)
    return redirect(url_for('admins.admin_login'))

# Delete News
@admin.route('/deletenews/<int:news_id>', methods=['POST'])
def deletenews(news_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            news = News.query.get_or_404(news_id)
            os.unlink(os.path.join(app.root_path, 'static/upload_pic', news.news_img))
            db.session.delete(news)
            db.session.commit()
            flash('News has been deleted!', 'success')
            return redirect(url_for('admins.admin_news'))
    return redirect(url_for('admins.admin_login'))

#Admin News Approvel
@admin.route('/approval')
def newsapproval():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            pending = News.query.filter_by(status='pending').all()
            approved = News.query.filter_by(status='approved').all()
            rejected = News.query.filter_by(status='rejected').all()
            return render_template('admin_news_approval.html', title="News-Approval", pending=pending, approved=approved, rejected=rejected)
    return redirect(url_for('admins.admin_login'))

# admin aprove and reject
@admin.route('/approval/<string:status>/<int:news_id>', methods=['POST'])
def approval(status, news_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            news = News.query.filter_by(id=news_id).first()
            if status == 'approve':
                news.status = 'approved'
                db.session.commit()
                flash('News has been Approved!', 'success')
                return redirect(url_for('admins.newsapproval'))
            elif status == 'rejected':
                news.status = 'rejected'
                db.session.commit()
                flash('News has been Rejected!', 'success')
                return redirect(url_for('admins.newsapproval'))
            else:
                pass
    return redirect(url_for('admins.admin_login'))

# Admin Feedback
@admin.route('admin-feedback')
def admin_feedback():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            feedback = Feedback.query.order_by(Feedback.date.desc()).all()
            return render_template('admin_feedback.html', title="feedback", feedback=feedback)
    return redirect(url_for('admins.admin_login'))

# Delete Feedback
@admin.route('/deletefeedback/<int:feedback_id>', methods=['POST'])
def deletefeedback(feedback_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            feedback = Feedback.query.get_or_404(feedback_id)
            db.session.delete(feedback)
            db.session.commit()
            flash('Feedback has been deleted!', 'success')
            return redirect(url_for('admins.admin_feedback'))
    return redirect(url_for('admins.admin_login'))


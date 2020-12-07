from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from news_portal import db, bcrypt
from news_portal.models import User, News, Feedback
from news_portal.admins.forms import AdminLoginForm

admin = Blueprint('admins', __name__)

#Admin login 
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

#Admin Logout
@admin.route('/admin_logout')
def admin_logout():
     logout_user()
     return redirect(url_for('admins.admin_login'))

#Admin dashboard
@admin.route('admin-home')
def admin_home():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            return render_template('admin_home.html', title="home")
    return redirect(url_for('admins.admin_login'))

#Admin User view
@admin.route('admin-user')
def admin_user():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            user = User.query.all()
            return render_template('admin_user.html', title="user", user=user)
    return redirect(url_for('admins.admin_login'))

# Delete User
@admin.route('/deleteuser/<int:user_id>', methods=['POST'])
def deleteuser(user_id):
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            usr = User.query.get_or_404(user_id)
            db.session.delete(usr)
            db.session.commit()
            flash('Your News has been deleted!', 'success')
            return redirect(url_for('admins.admin_user'))
    return redirect(url_for('admins.admin_login'))

#Admin News
@admin.route('admin-news')
def admin_news():
    if current_user.is_authenticated:
        if current_user.userole == 'admin':
            news = News.query.all()
            return render_template('admin_news.html', title="news", news=news)
    return redirect(url_for('admins.admin_login'))

#Admin Feedback
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
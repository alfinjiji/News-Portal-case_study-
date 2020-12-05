import os
import os.path as op
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from news_portal import app, db, bcrypt
from news_portal.models import User, News
from news_portal.users.forms import RegistrationForm, LoginForm, UserUpdate
from news_portal.main.utils import save_image
from news_portal.main.utils import current_datetime 

users = Blueprint('users', __name__)

# registration route
@users.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in register link is redirected to home  
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        fullname = form.fname.data +" "+form.lname.data
        user = User(name=fullname, mobile=form.mobile.data, email=form.email.data, address=form.address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are able to login ', 'register')
        return redirect(url_for('users.login')) # index.html function name is home
    return render_template('register.html', title='Register', form=form, time=current_datetime(1), date=current_datetime(2))

# login route
@users.route('/login', methods=['GET', 'POST'])
def login():
    # already login then it act as home page
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm() # create an object for class LoginForm
    if form.validate_on_submit():  #if we click the submit button perform the below tasks
        user = User.query.filter_by(email=form.email.data).first() # if entered email is in the db it will saved in user
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # if user exist and db password of user is equal to password enter in login form
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # args is an dictonery
            # if we search 'localhost/account' it will redirect to login and tell to login if we login it redirect to home 
            # by the below command it will redirect to account 
            # redirect to next page if next page exit else go to login page
            return redirect(next_page) if next_page else  redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessfull. Please check username and password', 'danger') 
    return render_template('login.html', title='Login', form=form, time=current_datetime(1), date=current_datetime(2)) # passing class object to login page

# logout route
@users.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('main.home'))

# Your account update route
@users.route('/account', methods=['GET', 'POST'])
@login_required  # if we try to access account page it will redirect to login page
def account():
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
        form.address.data = current_user.address
    image = url_for('static', filename='upload_pic/'+current_user.image)
    n = News.query.filter_by(uid=current_user.id).all()
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(uid=current_user.id).order_by(News.date.desc()).paginate(page=page, per_page=2)
    if n:
        msg=""
    else:
        msg="No news Added"
    return render_template('account.html', title='Your_Account', form=form, image=image, news=news, msg=msg, time=current_datetime(1), date=current_datetime(2))

#routes.py is for creating routes

from flask import render_template, url_for, flash, redirect, request
from news_portal import app, db, bcrypt
from news_portal.forms import RegistrationForm, LoginForm  # from form.py import class RegistrationForm and LoginForm
from news_portal.models import User # from package name.filename import classes
from flask_login import login_user, current_user, logout_user, login_required  # for logged an user in

@app.route('/')
def home():
    return render_template('index.html')

# registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in register link is redirected to home  
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        fullname = form.fname.data +" "+form.lname.data
        user = User(name=fullname, mobile=form.mobile.data, email=form.email.data, address=form.address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are able to login ', 'success')
        return redirect(url_for('login')) # index.html function name is home
    return render_template('register.html', title='Register', form=form)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # already login then it act as home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash('Login Unsuccessfull. Please check username and password', 'danger') 
    return render_template('login.html', title='Login', form=form) # passing class object to login page

# logout route
@app.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('home'))

# route redirect only is accound is loged in
@app.route('/account')
@login_required  # if we try to access account page it will redirect to login page
def account():
    return render_template('account.html', title='Account')
#routes.py is for creating routes
from flask import render_template, url_for, flash, redirect, request
import os
import secrets
from PIL import Image
from news_portal import app, db, bcrypt
from news_portal.forms import RegistrationForm, LoginForm, NewsForm, UserUpdate  # from form.py import class RegistrationForm and LoginForm
from news_portal.models import User, News # from package name.filename import classes
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

# save picture
def save_image(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img = random_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/upload_pic', img)
    output_size = (150, 150) #125x125px
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(img_path)
    return img

# Your account update route
@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
        form.address.data = current_user.address
    image = url_for('static', filename='upload_pic/'+current_user.image)
    return render_template('account.html', title='Your_Account', form=form, image=image)

# addnews route
@app.route('/addnews', methods=['GET', 'POST'])
@login_required
def addnews():
    form = NewsForm()
    if form.validate_on_submit():
        if form.news_img.data:
            img_file = save_image(form.news_img.data)
            img = img_file
        news = News(heading=form.heading.data, description=form.description.data, district=form.district.data, place=form.place.data, category=form.category.data, news_img=img, uid=current_user.id)
        db.session.add(news)
        db.session.commit()
        flash('Your News Uploaded Successfully!','success')
        return redirect(url_for('addnews'))
    news = News.query.filter_by(uid=current_user.id).all()
    return render_template('addnews.html', title='Add_News', form=form, news=news)
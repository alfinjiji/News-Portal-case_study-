USER AUTHENTICATION
-------------------
## for hashed password
// pip install flask-bcrypt

// python
// from flask_bcrypt import Bcrypt
// bcrypt = Bcrypt()

# encrypt password 'your password'
// bcrypt.generate_password_hash('your password').decode('utf-8')

# save hash password as variable
// paswd = bcrypt.generate_password_hash('your password').decode('utf-8')

# decrypt hashed password
// bcrypt.check_password_hash(paswd, 'your password')
                                |           |-- password that we enter
                                |-- variable name that we used to store hashed password

//# custom validation for check if enter same email that already register

    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')
    
# extention for login
// pip install flask-login

# add login in __init__.py
// from flask_login import LoginManager
// login_manager = LoginManager(app)

# add login_manager in models.py
// from flaskblog import login_manager

# function for get an user by id
@login_manager.user_loader   //extention will expect user model
def load_user(user_id):
    return User.query.get(int(user_id))

# inoder to perform login we need some cridential such as 'is_active, is_authenticate, is_anonimus, get_id 
# for all this we use a simple class called UserMixin
// from flask_login import UserMixin
# add UserMixin in User class as parameter along with db
// eg: class User(db.Model, UserMixin):

# modify login route
// from flask_login import login_user, current_user, logout_user, login_required

// 'login_manager' if the user is login then only go to corresponting route else go to login page 

___________________________________________________________________________________________________________________________________________

PACKAGE STRUCTURE
-----------------
// Structure application by using package

|--flaskblog                // package that we created
|   |
|   |-- static              // contain css, js, imgages etc. all static files
|   |       |-- style.css
|   |
|   |-- templates           // html files were kept in this folder
|   |       |-- index.html
|   |       |-- layout.html // contain the repeted terms
|   |       |-- login.html  // login page
|   |       |-- register.html // register page
|   |
|   |-- venv
|   |       |-- # virtual envionment files
|   |
|   |-- __init__.py     // initalizing the application
|   |-- forms.py        // for forms login and register
|   |-- models.py       // for creating models or tables
|   |-- routes.py       // for setting routes
|   |-- site.db         // our sqlite db
|
|--run.py       // pgm help to run this application


// create an folder here eg: flaskblog
// move every files in to this directory except our app.py
// create file __init__.py, routes.py, models.py in flaskblog folder
// make changes ....
// rename app.py to run.py

## Run application
//python app.py

## create db
// python
// from packagename import db 
//   eg: from flaskblog import db
// db.create_all()

// from packagename.filename import class name
//   eg: from flaskblog.models import Post, User
// User.query.all()

___________________________________________________________________________________________________________________________________________

DATABASE SQLALCHEMY SQLITE
--------------------------

pip install flask-sqlalchemy 
// flask-sqlalchemy is an flask specific sql extension 

//open the python shell by enter python in cmd

from 'your application file' import db 

eg: from app import db 

db.create_all()    // it will create an db file 

//for manually insert data in table
 from app import Class name
 eg : from app import User, Post

 user_1 = User(username='john', email='john@gmail.com', password='password')  // save the datas in variable user_1

 db.session.add(user_1) 
 db.session.commit()  // enter data in table

 User.query.all()  // showw all datas in db

 User.query.first() // show the first data

 User.query.filter_by(username="alfin").all()   // filter by username

 User.query.filter_by(username="alfin").first()  // return the first list that have username alfin

 user =  User.query.filter_by(username="alfin").all()  // store the datas in user which has username=alfin

 user.id  // will show id of user that store in user variable

 user = User.query.get(1) //get an element with id 1

 //insert data in post table

 post_1 = Post(title='blog', content='First post content', user_id=user.id')
 db.session.add(post_1)
 db.session.commit()
 user.posts

 for post in user.post:
    print(post.title)

post.author // will get entair details about user who post the post

db.drop_all()
db.create_all() // recreate db
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
DB_Name = 'market.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DB_Name
secret_key = os.urandom(12).hex()

app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='views.login_page'
login_manager.login_message_category='info'

# TODO:
#  1. a modal to create a new listing option for any user,
#  2. to change to another user ,
#  3. to add or subtract more fund to user account,



from .views import views # .view needs to import db, so this import needs to be after db's creation
app.register_blueprint(views, url_prefix='/')

# This following import has to be after db is created, otherwise, circular importing will be generated
from .models import Item
if not path.exists(f'/Market/{DB_Name}'):
    db.create_all(app=app)




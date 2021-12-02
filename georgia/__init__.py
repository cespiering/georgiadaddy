import os
from flask_mail import Mail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('GEORGIA_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///georgia'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)



# def connect_to_app(flask_app, )

from georgia import routes
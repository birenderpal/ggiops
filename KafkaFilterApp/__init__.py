from flask import Flask,session,g
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import datetime
#from KafkaFilterApp import auth


app = Flask(__name__, static_folder='static', template_folder='static/templates')

#from SmartsApp.auth.app_auth import appAuth_blueprint

app.config.from_object('KafkaFilterApp.config.config.TestConfig')
#app.register_blueprint(appAuth_blueprint)

bcrypt = Bcrypt(app)
db=SQLAlchemy(app)

login_manager = LoginManager(app=app)

from auth.app_auth import app_auth
app.register_blueprint(app_auth)

login_manager.login_view="auth.login"

from KafkaFilterApp.model.User import User


from KafkaFilterApp.views import routes
from KafkaFilterApp.api import routes

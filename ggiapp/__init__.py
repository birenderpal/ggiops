from flask import Flask,session,g
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import datetime
#from ggiapp import auth


app = Flask(__name__, static_folder='static', template_folder='static/templates')

#from SmartsApp.auth.app_auth import appAuth_blueprint

app.config.from_object('ggiapp.config.config.TestConfig')
#app.register_blueprint(appAuth_blueprint)

bcrypt = Bcrypt(app)
db=SQLAlchemy(app)

login_manager = LoginManager(app=app)

from auth.app_auth import app_auth
app.register_blueprint(app_auth)

login_manager.login_view="auth.login"

from ggiapp.model.User import User


from ggiapp.views import routes
from ggiapp.api import routes

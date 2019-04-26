from flask import Flask, session,g
import datetime
#from ggiapp import auth

app = Flask(__name__, static_folder='static', template_folder='static/templates')
from ggiapp.views import routes
from ggiapp.api import routes
#from SmartsApp.auth.app_auth import appAuth_blueprint

app.config.from_object('ggiapp.config.config.BaseConfig')
#app.register_blueprint(appAuth_blueprint)


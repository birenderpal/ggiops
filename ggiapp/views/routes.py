from ggiapp import app,login_manager
from flask_login import login_required
from flask import jsonify, request,json, render_template,redirect
#===============================================================================
# logging.config.fileConfig('logging.conf')
# LOGGER = logging.getLogger('splunk_query')s
#===============================================================================


@login_manager.user_loader
def load_user(id):
    print(User.query.get(id))
    return User.query.get(id);

@app.route('/')

def index():
    return render_template('index.1.html')

from ggiapp import app
from flask import jsonify, request,json, render_template,redirect
from ggiapp.controllers.SplunkApp import SplunkApp
#===============================================================================
# logging.config.fileConfig('logging.conf')
# LOGGER = logging.getLogger('splunk_query')
#===============================================================================


HOSTNAME="localhost:8000"

@app.route('/')

def index():
    return render_template('index.html')

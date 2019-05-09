from ggiapp import app
from flask import jsonify, request,json, render_template,redirect
#===============================================================================
# logging.config.fileConfig('logging.conf')
# LOGGER = logging.getLogger('splunk_query')s
#===============================================================================


HOSTNAME="localhost:8000"

@app.route('/')

def index():
    return render_template('index.html')

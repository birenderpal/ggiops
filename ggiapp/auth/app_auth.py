'''
Created on 23/04/2018

@author: t821012
'''
from SmartsApp import app,login
from flask import request,render_template,redirect,url_for,Blueprint,session,g,flash
from flask_login import current_user, login_user,logout_user, login_required
from SmartsApp.model.User import User
import ldap
from SmartsApp.views.routes import index
appAuth_blueprint = Blueprint(
    'appAuth', __name__,
    template_folder='templates',
    static_folder='static'
    )
@login.user_loader
def load_user(id):
    return User(id)
@appAuth_blueprint.before_request
def get_current_user():
    g.user = current_user

@appAuth_blueprint.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            username=request.form['username']
            password=request.form['password']
            
            try:
                user_name=User.get_user_name(username)                
            except:
                flash(
                'Invalid username. Please try again.',
                'danger')
                return render_template('login.html')            
            
            user=User(user_name)
            print(user.get_id())
            print(user)
            print(user.username)
            try:
                User.try_login(username,password)                
            except ldap.INVALID_CREDENTIALS:
                flash(
                'Incorrect password. Please try again.',
                'danger')                
                return render_template('login.html')            
            login_user(user,remember=False)
            next = request.args.get('next')
            print(next)
            return redirect(next or url_for('index'))
    else:
        return render_template('login.html')

@appAuth_blueprint.route('/logout',methods=['GET', 'POST'])    
@login_required
def logout():
    logout_user()
    return redirect(url_for('appAuth.login'))
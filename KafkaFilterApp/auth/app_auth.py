'''
Created on 23/04/2018

@author: t821012
'''
from KafkaFilterApp.model.User import User
from KafkaFilterApp import db,bcrypt,login_manager
from flask import request, render_template, redirect, url_for, Blueprint, g, flash,session,jsonify
from flask_login import current_user, login_user, logout_user, login_required
from KafkaFilterApp.views.routes import index
app_auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static'
)


@app_auth.before_request
def get_current_user():
    g.user = current_user

@login_manager.user_loader
def load_user(id):
    print(User.query.get(id))
    return User.query.get(id);

@app_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()            
            if not user:                
                return jsonify({'status':'register'})
            elif bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=False)
                return jsonify({'status':'success'})
            else:
                return jsonify({'status':'invalid password'})
    else:
        return render_template('login.html')


@app_auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status':'success'})


@app_auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(username,email,password)
        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user:
            #print(user)
            return jsonify({'status':'user exists'})
        elif user_email:
            return jsonify({'status':'email already in use'})
        else:
            new_user=User(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()            
            #return "User Added"
            return jsonify({'status':'success'})

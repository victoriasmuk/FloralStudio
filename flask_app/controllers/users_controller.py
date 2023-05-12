from flask import render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.bouquets_model import Bouquet
import os
from os import path

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    path = "/Users/victoriasmuk/Desktop/coding_dojo/FloralStudio/flask_app/static/images/flowers/"
    images = []
    for file in os.listdir(path):
        if file.endswith('.jpeg'):
            images.append(file)
    if 'uid' in session:
        user = session['uid']
    else:
        user = 0
    return render_template('index.html', images = images, user=user)

@app.route('/account/<int:user_id>')
def account_info(user_id):
    user = User.get_user_by_id(user_id)

    if not 'uid' in session:
        flash('Please sign in first!')
        return redirect('/login')
    
    return render_template('account.html', user=user)

@app.route('/update_user', methods = ['POST'])
def update_user():
    if not 'uid' in session:
        flash('Please sign in first!')
        return redirect('/login')
    if not User.validate_update(request.form):
        user_id = request.form['id']
        return redirect(url_for('account_info', user_id=user_id))
    User.update(request.form)
    user_id = request.form['id']
    return redirect(url_for('account_info', user_id=user_id))

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/register')
def create_account():
    return render_template('register.html')


@app.route('/login_page', methods=['POST'])
def login():
    logged_in_user = User.login(request.form)
    if logged_in_user:
        session['uid'] = logged_in_user.id
        return redirect(url_for('account_info', user_id=session['uid']))
    return redirect('/login')

@app.route('/register_page', methods=['POST'])
def register():
    valid_user = User.validate(request.form)
    if not valid_user:
        return redirect('/register')
    new_user = User.create(request.form)
    session['uid'] = new_user.id
    return redirect('/account')

@app.route('/about_us')
def about():
    if 'uid' in session:
        user = session['uid']
    else:
        user = 0
    return render_template('about_us.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
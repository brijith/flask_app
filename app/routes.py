from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from flask import request
from app import db
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Brijith'}
    posts = [
        {
            'auther': {'username': 'Anisha'},
            'body': 'It is a beautiful day !'
        },
        {
            'auther': {'username': 'Brijith'},
            'body': 'Yes It is a beautiful day!'
        }
    ]
    return render_template('index.html',title='welcome', user=user, posts=posts)

@app.route('/posts')
@login_required
def posts():
    return '<h1>posts will come here</h1>'

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body': 'Test post 1'},
        {'author':user, 'body': 'Test post 2'},
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account for {} has beed created'.format(user.username))
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register new User', form=form)
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): ### on login form submit!!
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid credential!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign in', form=form) ## login form load


@app.route('/edit_profile', methods= ['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile is updated !')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    else:
        flash('Something went wrong!!!')
    return render_template('edit_profile.html', title="Edit Profile", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

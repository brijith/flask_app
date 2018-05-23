from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): ### on login form submit!!
        user = User.query.filter_by(username=form.username.data).first()
        print user
        if user is None or not user.check_password(form.password.data):
            flash('invalid credential!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form) ## login form load

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

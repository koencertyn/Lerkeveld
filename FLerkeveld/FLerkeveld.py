#!/usr/bin/env python2

# -*- coding: utf-8 -*-
"""
    Flerkeveld
    ~~~~~~
    A website made using Flask and Materialize.

"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import flask.ext.login as flask_login

navbar_links = [("index","Home","/"),
                ("wie","Over ons","/wie"),
                ("lied","Lerkeveld Lied","/lied"),
                ("contact","Contact","/contact")]



# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('LERKIESSITE_SETTINGS', silent=True)


### LOGIN MANAGER ###


# initiate login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'butt': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    def __init__(self):
        self._is_active = True
        self._is_anonymous = False
        self._is_authenticated = True

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

    @property
    def is_anonymous(self):
        return self._is_anonymous

    @is_anonymous.setter
    def is_anonymous(self, value):
        self._is_anonymous = value

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')



@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def login_request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['pw']

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='password' id='password' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''


    user = login_request_loader(request)
    if user is None:
        return "foute email"
    elif user.is_authenticated:
        flask_login.login_user(user)
        return redirect(url_for('protected'))
    else:
        return 'Bad login'

@app.route('/alogin', methods=['GET', 'POST'])
def alogin():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


### DATABASE ###



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


#@app.cli.command('initdb')
#def initdb_command():
#    """Creates the database tables."""
#    init_db()
#    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()




### WEBSITE ###



@app.route('/')
def show_entries():
    return render_template('index.html',navbar_links=navbar_links)
@app.route('/wie')
def wie_zijn_we():
    return render_template('wie.html',navbar_links=navbar_links)
@app.route('/lied')
def lied():
    return render_template('lied.html',navbar_links=navbar_links)
@app.route('/leden')
def leden():
    return render_template('leden.html',navbar_links=navbar_links)
@app.route('/contact')
def contact():
    return render_template('contact.html',navbar_links=navbar_links)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

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
    app.run(host="0.0.0.0")

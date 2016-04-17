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
                ("over_ons","Over ons","/over_ons"),
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
@app.route('/over_ons')
def over_ons():
    return render_template('over_ons.html',navbar_links=navbar_links)
@app.route('/lied')
def lied():
    return render_template('lied.html',navbar_links=navbar_links)
@app.route('/leden')
def leden():
    return render_template('leden.html',navbar_links=navbar_links)
@app.route('/contact')
def contact():
    return render_template('contact.html',navbar_links=navbar_links)
@app.route('/praesidium')
def praesidium():
    return render_template('praesidium.html',navbar_links=navbar_links)
@app.route('/oudPraesidia')
def oudPraesidia():
    return render_template('oudPraesidia.html',navbar_links=navbar_links)
@app.route('/praesidium2008')
def praesidium2008():
    return render_template('praesidium2008.html',navbar_links=navbar_links)
@app.route('/praesidium2009')
def praesidium2009():
    return render_template('praesidium2009.html',navbar_links=navbar_links)
@app.route('/praesidium2010')
def praesidium2010():
    return render_template('praesidium2010.html',navbar_links=navbar_links)
@app.route('/praesidium2012')
def praesidium2012():
    return render_template('praesidium2012.html',navbar_links=navbar_links)
@app.route('/praesidium2013')
def praesidium2013():
    return render_template('praesidium2013.html',navbar_links=navbar_links)
@app.route('/praesidium2014')
def praesidium2014():
    return render_template('praesidium2014.html',navbar_links=navbar_links)

if __name__ == '__main__':
    app.run(host="0.0.0.0")

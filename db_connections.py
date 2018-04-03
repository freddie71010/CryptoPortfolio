import sqlite3
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, \
	 render_template, flash
from app import *


def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(flask_app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'gdax_db'):
		g.gdax_db = connect_db()
	return g.gdax_db


@flask_app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'gdax_db'):
		g.gdax_db.close()

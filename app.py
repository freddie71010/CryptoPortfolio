import os
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, \
	render_template, flash
import db_connections

from dash import Dash
from dash_graph import setup_dash_app


flask_app = Flask(__name__)
dash_app = Dash(server=flask_app, url_base_pathname='/dash')

dash_app = setup_dash_app(dash_app)

# Load default config and override config from an environment variable for flask
flask_app.config.update(dict(
	DATABASE=os.path.join(flask_app.root_path, 'local_db_celery_test/gdax.db'),
	SECRET_KEY='5wutojw3;4oiw4nrasfigjh24waor',
	USERNAME='admin',
	PASSWORD='default'
))


@flask_app.route('/graph')
def graph_all():
	db = db_connections.get_db()
	query = '''
		SELECT price, trans_time 
		FROM prices
		'''
	coin_data = db.execute(query)
	return render_template('graph.html', coin_data=coin_data, coin='All')


@flask_app.route('/graph/<coin>')
def graph(coin):
	db = db_connections.get_db()
	query = '''
		SELECT price, trans_time 
		FROM prices
		WHERE coin = ?
		'''
	args = (coin.upper(),)
	coin_data = db.execute(query, args)
	return render_template('graph.html', coin_data=coin_data, coin=coin)


@flask_app.route('/')
def index():
	return render_template('base.html')


if __name__ == '__main__':
	flask_app.run(port=5000, debug=True)

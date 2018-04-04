import os
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, \
	render_template, flash
import sqlite3
from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html

flask_app = Flask(__name__)
dash_app = Dash(server=flask_app, url_base_pathname='/dash')

# Load default config and override config from an environment variable for flask
flask_app.config.update(dict(
	DATABASE=os.path.join(flask_app.root_path, 'local_db_celery_test/gdax.db'),
	SECRET_KEY='5wutojw3;4oiw4nrasfigjh24waor',
	USERNAME='admin',
	PASSWORD='default'
))

# ====================================================================================

dash_app.layout = html.Div(children=[
	html.P(children=["Hello P, these are children",
		html.H1("Hello H1, these are children"),
	]),

	dcc.Graph(
		id='cum-graph',
		figure={
			'data': [
				{'x': [1, 2, 3, 4], 'y': [4, 1, 2, 6], 'type': 'bar', 'name': 'SF'},
				{'x': [1, 2, 3, 4], 'y': [2, 4, 5, 2], 'type': 'bar', 'name': u'Montréal'},
			],
			'layout': {
				'title': 'Cumulative Graph',
				'plot_bgcolor': '#7FDBFF',
			},
		},
	),

	html.Label('Dropdown'),
	dcc.Dropdown(
		options=[{'label': x, 'value': x} for x in ['BTC', 'ETH', 'LTC']],
	),

	dcc.Input(id='input', value='Enter something', type='text'),
	html.Div(id='output')
])

@dash_app.callback(
	Output(component_id='output', component_property='children'),
	[Input(component_id='input', component_property='value')]
)
def update_value(input_data):
	try:
		return str(float(input_data)**2)
	except:
		return "Some error"


# ====================================================================================
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
# ====================================================================================


@flask_app.route('/graph')
def graph_all():
	db = get_db()
	query = '''
		SELECT price, trans_time 
		FROM prices
		'''
	coin_data = db.execute(query)
	return render_template('graph.html', coin_data=coin_data, coin='All')


@flask_app.route('/graph/<coin>')
def graph(coin):
	db = get_db()
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

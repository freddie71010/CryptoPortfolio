from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
from db_connections import *
import sqlite3
from flask import g

def setup_dash_app(dash_app):
	dash_app.layout = html.Div(children=[
		html.P(children=["Hello P, these are children",
			html.H1("Hello H1, these are children"),
		]),

		cum_graph(),

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
	
	return dash_app


def cum_graph():
	return dcc.Graph(
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
	)


# def spec_coin_data(coin):
# 	db = db_connections.get_db()
# 	query = '''
# 		SELECT price, trans_time 
# 		FROM prices
# 		WHERE coin = ?
# 		'''
# 	args = (coin.upper(),)
# 	coin_data = db.execute(query, args)
# 	for k, v in coin_data:
# 		print(k, v)
# 	return coin_data



# def connect_db():
# 	"""Connects to the specific database."""
# 	rv = sqlite3.connect(flask_app.config['DATABASE'])
# 	rv.row_factory = sqlite3.Row
# 	return rv


# def get_db():
# 	"""Opens a new database connection if there is none yet for the
# 	current application context.
# 	"""
# 	if not hasattr(g, 'gdax_db'):
# 		g.gdax_db = connect_db()
# 	return g.gdax_db


# @flask_app.teardown_appcontext
# def close_db(error):
# 	"""Closes the database again at the end of the request."""
# 	if hasattr(g, 'gdax_db'):
# 		g.gdax_db.close()
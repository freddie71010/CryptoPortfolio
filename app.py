import os
# from flask import Flask
# from flask import request, session, g, redirect, url_for, abort, \
# 	render_template, flash
from dash import Dash
from dash.dependencies import Input, State, Output
import dash_core_components as dcc
import dash_html_components as html
from db_connections import *

flask_app = Flask(__name__)
dash_app = Dash(server=flask_app, url_base_pathname='/dash')

# Load default config and override config from an environment variable for flask
flask_app.config.update(dict(
	DATABASE=os.path.join(flask_app.root_path, 'local_db_celery_test/gdax.db'),
	SECRET_KEY='5wutojw3;4oiw4nrasfigjh24waor',
	USERNAME='admin',
	PASSWORD='default'
))

dash_app.layout = html.Div(children=[
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

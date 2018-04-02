import os
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, \
	render_template, flash
from db_connections import *

app = Flask(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'local_db_celery_test/gdax.db'),
	SECRET_KEY='5wutojw3;4oiw4nrasfigjh24waor',
	USERNAME='admin',
	PASSWORD='default'
))


@app.route('/graph')
def graph_all():
	db = get_db()
	query = '''
		SELECT price, trans_time 
		FROM prices
		'''
	coin_data = db.execute(query)
	return render_template('graph.html', coin_data=coin_data, coin='All')


@app.route('/graph/<coin>')
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


@app.route('/')
def index():
	return render_template('base.html')


if __name__ == '__main__':
	app.run(port=5000, debug=True)

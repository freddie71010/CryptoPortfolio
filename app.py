import os
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, \
	render_template, flash, json, jsonify
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
	db = get_db().cursor()
	query = '''
		SELECT price, trans_time 
		FROM prices
		'''
	coin_data = db.execute(query)
	return render_template('graph.html', coin_data=coin_data, coin='All')


@app.route('/graph/<coin>')
def graph(coin):
	return render_template('graph.html', coin=coin)

@app.route('/graph/get_data')
def get_data(coin="BTC"):
	query = '''
	SELECT price, trans_time 
	FROM prices
	WHERE coin = ?
	'''
	args = (coin.upper(),)
	my_query = _query_db(query, args)
	print("GET_DATA:\n", my_query)
	return jsonify(my_query)

def _query_db(query, args=(), one=False):
	cur = get_db().cursor()
	cur.execute(query, args)
	r = [dict((cur.description[i][0], value) \
		for i, value in enumerate(row)) for row in cur.fetchall()]
	cur.connection.close()
	return (r[0] if r else None) if one else r


@app.route('/')
def index():
	return render_template('base.html')


if __name__ == '__main__':
	app.run(port=5000, debug=True)

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
	# db = get_db()
	# c = db.cursor()
	query = '''
		SELECT price, trans_time 
		FROM prices
		WHERE coin = ?
		'''
	args = (coin.upper(),)
	# c.execute(query, args)
	# coin_data_raw = c.fetchall()
	# price, trans_time = [], []
	# # print("COIN_DATA_raw:\n")
	# # for row in coin_data_raw:
	# # 	print(row['price'], row['trans_time'])
	# # print("="*50)

	# for row in coin_data_raw:
	# 	price.append(row['price'])
	# 	trans_time.append(row['trans_time'])
	# coin_data = {
	# 	'price': price,
	# 	'trans_time': trans_time,
	# }
	my_query = _query_db(query, args)
	print(my_query)
	json_output = json.dumps(my_query)
	return render_template('graph.html', coin_data=json_output, coin=coin)


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

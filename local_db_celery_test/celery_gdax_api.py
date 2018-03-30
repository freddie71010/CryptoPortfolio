import requests
from datetime import datetime
from create_db import create_connection


ALL_COINS = ['BTC-USD', 'ETH-USD', 'LTC-USD']


def download_gdax_data():
	coinbase_api_links = [
				'https://api.gdax.com/products/BTC-USD/ticker',
				'https://api.gdax.com/products/ETH-USD/ticker',
				'https://api.gdax.com/products/LTC-USD/ticker'
				]

	ticker_data = {}
	for link in coinbase_api_links:
		# print("link:", link, end='\n')
		r = requests.get(link)
		coin_info = r.json()
		# print("coin_info:", coin_info, end='\n')
		ticker_data[link[-14:-7]] = coin_info
	print("ticker_data:", ticker_data, end='\n\n')
	return ticker_data


def update_db_data(data):
	# Opens a connection
	conn = create_connection()
	# Sets up a cursor
	c = conn.cursor()
	# Creates SQL query for updating DB
	trans_time = datetime.now().isoformat()
	for coin in data.keys():
		if coin not in ALL_COINS:
			continue
		sql = '''
			INSERT INTO prices(exchange, coin, price, trading_pair, trans_time)
			VALUES (?, ?, ?, ?, ?)
			'''
		values = (
			"GDAX",
			coin.split('-')[0],
			data[coin]['price'],
			coin,
			trans_time
			)
		c.execute(sql, values)
		print("SQL run for: ", coin)
	conn.commit()
	conn.close()


def main():
	print("Downloading data...")
	gdax = download_gdax_data()
	update_db_data(gdax)
	print("Successfully added to DB!")



if __name__ == '__main__':
	main()

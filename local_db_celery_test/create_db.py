import sqlite3
from sqlite3 import Error



def create_connection():
	""" create a database connection to the SQLite database
	specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	database = "gdax.db"
	try:
		conn = sqlite3.connect(database)
		return conn
	except Error as e:
		print(e)
	return None

def create_table(conn, create_table_sql):
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def main():
	drop_prices_tbl = """DROP TABLE prices;"""
	sql_create_price_tbl = """
							CREATE TABLE prices (
								id integer PRIMARY KEY,
								exchange text NOT NULL,
								coin text NOT NULL,
								price float NOT NULL,
								trading_pair text NOT NULL,
								trans_time text NOT NULL
								);"""
	conn = create_connection()
	if conn is not None:
		create_table(conn, drop_prices_tbl)
		print("Dropped table: prices")
		create_table(conn, sql_create_price_tbl)
		print("Created table: prices")
	else:
		print("Error creating database connection.")
	return


if __name__ == "__main__":
	main()

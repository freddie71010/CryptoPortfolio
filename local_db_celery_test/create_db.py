import sqlite3
from sqlite3 import Error


def create_connection(db_file):
	""" create a database connection to the SQLite database
	specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
		# return conn
	except Error as e:
		print(e)
	finally:
		conn.close()


def create_table(conn, create_table_sql):
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	pass

if __name__ == "__main__":
	create_connection("gdax.db")
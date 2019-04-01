from sql_functions import commit_sql

def drop_tables(sql_connection):
	query = (
	"""
	DROP TABLE IF EXISTS products CASCADE;
	DROP TABLE IF EXISTS sessions CASCADE;
	DROP TABLE IF EXISTS visitors CASCADE;
	DROP TABLE IF EXISTS orders CASCADE;
	DROP TABLE IF EXISTS viewed_before CASCADE;
	DROP TABLE IF EXISTS recommendations CASCADE;
	DROP TABLE IF EXISTS buids CASCADE;
	""" )
	return commit_sql(sql_connection, query)

def create_tables(sql_connection):
	query = (
	"""
	CREATE TABLE products (
		product_id VARCHAR(255) PRIMARY KEY NOT NULL,
		name VARCHAR(255) NOT NULL,
		brand VARCHAR(255) NOT NULL,
		gender VARCHAR(255) NOT NULL,
		doelgroep VARCHAR(255) NOT NULL,
		category VARCHAR(255) NOT NULL,
		sub_category VARCHAR(255) NOT NULL,
		sub_sub_category VARCHAR(255) NOT NULL,
		selling_price FLOAT NOT NULL,
		availability INTEGER NOT NULL );
		
	CREATE TABLE visitors (
		visitor_id VARCHAR(255) PRIMARY KEY NOT NULL );
		
	CREATE TABLE sessions (
		session_id VARCHAR(255) PRIMARY KEY NOT NULL,
		buid VARCHAR(255) NOT NULL,
		session_start VARCHAR(255) NOT NULL,
		session_end VARCHAR(255) NOT NULL );
		
	CREATE TABLE orders (
		session_id VARCHAR(255) NOT NULL,
		product_id VARCHAR(255) NOT NULL );
	
	CREATE TABLE previously_recommended(
		visitor_id VARCHAR(255) NOT NULL,
		product_id VARCHAR(255) NOT NULL );
		
	CREATE TABLE viewed_before(
		visitor_id VARCHAR(255) NOT NULL,
		product_id VARCHAR(255) NOT NULL );
	
	CREATE TABLE buids(
		visitor_id VARCHAR(255) NOT NULL,
		buid VARCHAR(255) PRIMARY KEY NOT NULL);
	""" )
	return commit_sql(sql_connection, query)

def alter_tables(sql_connection):
	query = (
	"""
	AlTER TABLE sessions
		ADD FOREIGN KEY (buid) REFERENCES buids(buid);
	AlTER TABLE orders	
		ADD FOREIGN KEY (product_id) REFERENCES products(product_id);
	AlTER TABLE buids	
		ADD FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id);
	AlTER TABLE previously_recommended	
		ADD FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id),
		ADD FOREIGN KEY (product_id) REFERENCES products(product_id);
	AlTER TABLE viewed_before
		ADD FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id),
		ADD FOREIGN KEY (product_id) REFERENCES products(product_id);
	""")
	return commit_sql(sql_connection, query)
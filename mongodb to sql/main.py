import timeit # voor het meten van runtime
from sql_tables import drop_tables, create_tables, alter_tables
from mongo_download import insert_files
from databases import connect_sql, mdb_connectie, drop_create_database

def menu(sql_db,mongo_db):
	## limit to insert files
	limit = 100000
	
	## sql tables
	drop_tables(sql_db)
	create_tables(sql_db)
	alter_tables(sql_db)

	## insert files in SQL with arguments: (mongodbconnection, mongodbcolname, sqlconnection, table_functionname, limit)
	insert_files(mongo_db,'products', sql_db, 'insert_products', limit)
	insert_files(mongo_db,'visitors', sql_db, 'insert_visitors', limit)
	insert_files(mongo_db,'visitors', sql_db, 'insert_previously_recommended', limit)
	insert_files(mongo_db,'visitors', sql_db, 'insert_viewed_before', limit)
	insert_files(mongo_db,'sessions', sql_db, 'insert_orders', limit)
	insert_files(mongo_db,'visitors', sql_db, 'insert_buids', limit)
	insert_files(mongo_db,'sessions', sql_db, 'insert_sessions', limit)
	
if __name__== "__main__":
	## Create database and start connections
	drop_create_database('voordeelshop', 'postgres', 'postgres', 'Welkom01!')
	sql_db = connect_sql('voordeelshop', 'postgres', 'Welkom01!')
	mongo_db = mdb_connectie('voordeelshop')
	## start menu
	menu(sql_db,mongo_db)
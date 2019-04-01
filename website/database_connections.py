import psycopg2
from pymongo import MongoClient

## mongodb database connectie
def mdb_connectie(dbname):
	mongo_db = MongoClient()
	mydb = mongo_db[dbname]
	return mydb
	
## SQL database connectie
def connect_sql(dbname, dbuser, dbpass):
	sql_db = psycopg2.connect("dbname={} user={} password={}".format(dbname, dbuser, dbpass))
	return sql_db
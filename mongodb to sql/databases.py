import psycopg2
from pymongo import MongoClient


# controleert of database bestaat
def database_exist(dbname, dbuser, dbpassword):
    'See if inserted databae exist'
    try:
        sql_db = psycopg2.connect(
            "dbname={} user={} password={}".format(dbname, dbuser, dbpassword))  # connect to database
        return 1
    except:
        return 0


# drop and create SQL database
def drop_create_database(dbname, dbrootname, dbuser, dbpassword):
    'Drop and create database if exist'
    exist = database_exist(dbname, dbuser, dbpassword)
    sql_db = psycopg2.connect(
        "dbname={} user={} password={}".format(dbrootname, dbuser, dbpassword))  # connect to database
    cur = sql_db.cursor()
    sql_db.autocommit = True
    # ----Check if database exist in.If exist execute the first 3 cur.executes, else create db
    if exist == 1:
        cur.execute('REVOKE CONNECT ON DATABASE {} FROM public;'.format(dbname))
        cur.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{}';".format(dbname))
        cur.execute('DROP DATABASE IF EXISTS {}'.format(dbname))
    cur.execute('CREATE DATABASE {}'.format(dbname))
    sql_db.autocommit = False
    cur.close()


# mongodb database connectie
def mdb_connectie(dbname):
    mydb = MongoClient()
    mongo_db = mydb[dbname]
    return mongo_db


# SQL database connectie
def connect_sql(dbname, dbuser, dbpassword):
    sql_db = psycopg2.connect("dbname={} user={} password={}".format(dbname, dbuser, dbpassword))
    return sql_db

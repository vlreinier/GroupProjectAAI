import psycopg2


# Voert search query uit, en returned de resultaten
def search_sql(sql_db, query):
    try:
        cur = sql_db.cursor()
        cur.execute(query)
        fetched = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return fetched


# Voert de commit query uit
def commit_sql(sql_db, query):
    try:
        cur = sql_db.cursor()
        cur.execute(query)
        cur.close()
        sql_db.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

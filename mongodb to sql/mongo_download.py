import sql_inserts
from sql_functions import commit_sql
import sys
import time

# download en roept insert SQL function aan om de 10000 bestanden
def insert_files(mongodb_connection, mongodbcollection, sql_connection, table_functionname, limit):
    start = time.time()
    my_col = getattr(mongodb_connection, mongodbcollection)
    function_to_call = getattr(sql_inserts, table_functionname)
    collection_count = my_col.count()
    if collection_count > limit:
        collection_count = limit
    print(table_functionname, 'is started!')
    files = []
    count = inserted = 0

    for file in my_col.find().limit(limit):
        files.append(file)
        count += 1

        if count - inserted == 10000:
            inserts = function_to_call(files, sql_connection, '')
            if inserts != '':
                commit_sql(sql_connection, inserts)
            files = []
            inserted = count
        if collection_count == count:
            inserts = function_to_call(files, sql_connection, '')
            if inserts != '':
                commit_sql(sql_connection, inserts)

    print(table_functionname, 'is finished, runtime in seconds:  ', round((time.time() - start), 3), '\n')

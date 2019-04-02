from sql_commit_query import search_sql
from get_products import get_product_details
from related_products import content_tree
import random

## functie voor het sorteren van een lijst met tuples van groot naar klein op index 1, tweede element in tuple
def sort_big_to_small_on_index_one(id_list):
	final_list = []
	sorted_id_list = sorted(id_list, key=lambda tup: tup[1],reverse=True)
	for product_id in sorted_id_list:
		final_list.append(product_id[0])
	return final_list

## functie voor het ophalen populaire / meest verkochte producten, staat op homepagina
def popular(sql_connection, mongo_db, sessiondata):
    total_cartproducts = len(sessiondata)
    get_similar_products = 1
    if total_cartproducts in range(1,3):
        get_similar_products = 5
    if total_cartproducts in range(3,5):
        get_similar_products = 2

    personal = []
    for product_id in sessiondata:
        product_details = search_sql(sql_connection,"SELECT category, sub_category, gender FROM products WHERE product_id = '{}'".format(product_id))[0]
        category = product_details[0]
        sub_category = product_details[1]
        gender = product_details[2]
        query_results = search_sql(sql_connection, "SELECT product_id FROM products WHERE category = '{}' AND sub_category = '{}' AND gender= '{}' ORDER BY RANDOM() LIMIT {}".format(category, sub_category, gender, get_similar_products))
        for tuple in query_results:
            personal.append(tuple[0])

    popular = []
    query_results = search_sql(sql_connection, "SELECT orders.product_id, COUNT(*) AS populair FROM sessions INNER JOIN orders ON sessions.session_id = orders.session_id WHERE sessions.session_start > '2018-10-23 11:57:54.914000' GROUP BY orders.product_id ORDER BY populair DESC LIMIT 200")

    for tuple in query_results:
        popular.append(tuple[0])

    if len(personal) < 5:
        popular = random.sample(popular, 10 - len(personal))
    else:
        popular = random.sample(popular, 5)
    id_list = personal + popular
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van persoonlijke aanbevelingen bezoekersid a.d.h.v. eerder bekeken en gelijke producten
def personal(sql_db,mongo_db,sessiondata):
    id_list = []
    query_results1 = search_sql(sql_db,"SELECT orders.product_id FROM visitors INNER JOIN buids on visitors.visitor_id = buids.visitor_id INNER JOIN sessions on buids.buid = sessions.buid INNER JOIN orders on sessions.session_id = orders.session_id WHERE visitors.visitor_id = '{}'".format(sessiondata['_id']))
    for product_id in query_results1:
        id_list.append(product_id[0])
    id_list = content_tree(sql_db, id_list)
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def collaborative(sql_db,mongo_db,sessiondata):
    id_list = []
    for product_id in sessiondata:
        query_results = search_sql(sql_db,"SELECT related, lift FROM lift_products WHERE product_id = '{}' ORDER BY lift DESC".format(product_id))
        for result in query_results:
	        id_list.append(result[0])
    sorted_id_list = sort_big_to_small_on_index_one(id_list)
    return get_product_details(mongo_db, sorted_id_list, False)

## functie voor het ophalen van soortgelijk product aanbevelingen a.d.h.v. opgeslagen producten
def content(sql_db,mongo_db,sessiondata):
	id_list = content_tree(sql_db, sessiondata)
	return get_product_details(mongo_db, id_list, True)
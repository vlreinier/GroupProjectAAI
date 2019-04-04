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
    visitor_id = sessiondata['visitor_id']
    if visitor_id != '':
        include_personal = True

    popular = []
    popular_orders_last_2months = search_sql(sql_connection, """SELECT orders.product_id, COUNT(*) AS populair FROM sessions
                                                                INNER JOIN orders ON sessions.session_id = orders.session_id
                                                                WHERE sessions.session_start > CURRENT_DATE - INTERVAL '2 months'
                                                                GROUP BY orders.product_id ORDER BY populair DESC LIMIT 150""")
    popular_viewed_last_month = search_sql(sql_connection, """SELECT viewed_before.product_id FROM viewed_before
                                                              INNER JOIN visitors ON viewed_before.visitor_id = visitors.visitor_id
                                                              INNER JOIN buids ON visitors.visitor_id = buids.visitor_id
                                                              INNER JOIN sessions ON buids.buid = sessions.buid
                                                              WHERE sessions.session_start > CURRENT_DATE - INTERVAL '1 month'
                                                              GROUP BY viewed_before.product_id
                                                              ORDER BY COUNT(viewed_before.product_id) DESC LIMIT 10""")
    for tuple in popular_orders_last_2months:
        popular.append(tuple[0])
    for tuple in popular_viewed_last_month:
        popular.append(tuple[0])

    popular = random.sample(popular, 5)
    id_list = popular # + personal
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van persoonlijke aanbevelingen bezoekersid a.d.h.v. eerder bekeken en gelijke producten
def personal(sql_db,mongo_db,sessiondata):
    id_list = []
    query_results1 = search_sql(sql_db,"SELECT orders.product_id FROM visitors INNER JOIN buids on visitors.visitor_id = buids.visitor_id INNER JOIN sessions on buids.buid = sessions.buid INNER JOIN orders on sessions.session_id = orders.session_id WHERE visitors.visitor_id = '{}'".format(sessiondata['visitor_id']))
    for product_id in query_results1:
        id_list.append(product_id[0])
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def collaborative(sql_db,mongo_db,sessiondata):
    id_list = []
    for product_id in sessiondata:
        query_results = search_sql(sql_db,"SELECT related, lift FROM lift_products WHERE product_id = '{}' ORDER BY lift DESC".format(product_id))
        for result in query_results:
	        id_list.append(result)
    sorted_id_list = sort_big_to_small_on_index_one(id_list)
    return get_product_details(mongo_db, sorted_id_list, False)

def shoppingcart(sql_db, mongo_db, sessiondata):
    id_list = []
    for id in sessiondata:
        id_list.append(str(id))
    return get_product_details(mongo_db, id_list, False)

def loadselected(sql_db, mongo_db, sessiondata):
    id_list = []
    for id in sessiondata:
        id_list.append(str(sessiondata[id]))
    return get_product_details(mongo_db, id_list, False)

## functie voor het ophalen van soortgelijk product aanbevelingen a.d.h.v. opgeslagen producten
def selectedsimilar(sql_db,mongo_db,sessiondata):
	id_list = content_tree(sql_db, sessiondata)
	return get_product_details(mongo_db, id_list, False)
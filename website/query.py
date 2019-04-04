from sql_commit_query import search_sql
from get_products import get_product_details
from related_products import content_tree, get_popular_products, personal_preffered_products
import random

## functie voor het ophalen populaire / meest verkochte producten, staat op homepagina
def popular(sql_connection, mongo_db, visitor_id):
    personal_all = personal_preffered_products(sql_connection, visitor_id)
    popular_all = get_popular_products(sql_connection, visitor_id)
    if len(personal_all) < 3:
        personal_all = random.sample(personal_all, len(personal_all))
        popular_all = random.sample(popular_all, 3 + (3-len(personal_all)))
    else:
        personal_all = random.sample(personal_all, 3)
        popular_all = random.sample(popular_all, 3)
    id_list = popular_all + personal_all
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van persoonlijke aanbevelingen bezoekersid a.d.h.v. eerder bekeken en gelijke producten
def personal(sql_connection,mongo_db,visitor_id):
    id_list = personal_preffered_products(sql_connection, visitor_id)
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def collaborative(sql_db,mongo_db,sessiondata):
    id_list = []
    for product_id in sessiondata:
        query_results = search_sql(sql_db,"SELECT related, lift FROM lift_products WHERE product_id = '{}' ORDER BY lift DESC".format(product_id))
        for result in query_results:
	        id_list.append(result[0])
    return get_product_details(mongo_db, id_list, False)

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
    id_list = []
    for i in sessiondata:
        id_list.append(i)
    id_list = content_tree(sql_db, sessiondata)
    return get_product_details(mongo_db, id_list, False)
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
    if len(sessiondata) == 1:
        limit = 6
    elif len(sessiondata) == 2:
        limit = 3
    elif len(sessiondata) == 3 or 4:
        limit = 2
    else:
        limit = 1
    for product_id in sessiondata:
        query_results = search_sql(sql_db,"SELECT related, lift FROM lift_products WHERE product_id ='{}' ORDER BY lift DESC limit {}".format(product_id, limit))
        for result in query_results:
            id_list.append(result[0])
        if len(query_results) != limit:
            product_price = search_sql(sql_db, "SELECT selling_price FROM products WHERE product_id='{}'".format(product_id))
            limit_cat = limit - len(query_results)
            product_cat = search_sql(sql_db, "SELECT category FROM products WHERE product_id='{}'".format(product_id))
            query_results_cat = search_sql(sql_db, "SELECT product_id FROM products WHERE category='{}' AND selling_price BETWEEN {}*0.8 AND {}*1.2 ORDER BY RANDOM() LIMIT {}".format(product_cat[0][0], product_price, product_price, limit_cat))
            for result_cat in query_results_cat:
                id_list.append(result_cat[0])
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
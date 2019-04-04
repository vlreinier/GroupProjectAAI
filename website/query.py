from sql_commit_query import search_sql
from get_products import get_product_details
from related_products import content_tree
import random
from statistics import mode

def get_highest_occurence(id_list):
    new_list = []
    category = {}
    sub_category = {}
    brand = {}
    gender = {}
    for i in id_list:
        category[i[0]] = i[1]
        sub_category[i[0]] = i[2]
        brand[i[0]] = i[3]
        gender[i[0]] = i[4]
    most_category = mode(category.values())
    most_sub_category = mode(sub_category.values())
    most_brand = mode(brand.values())
    most_gender = mode(gender.values())
    for i in category:
        if category[i] == most_category:
            new_list.append(i)
    for i in sub_category:
        if sub_category[i] == most_sub_category:
            new_list.append(i)
    for i in brand:
        if brand[i] == most_brand:
            new_list.append(i)
    for i in gender:
        if gender[i] == most_gender:
            new_list.append(i)
    return set(new_list)

def personal_transactions(sql_connection, visitor_id):
    ordered = search_sql(sql_connection,"""SELECT orders.product_id, products.category,products.sub_category, products.brand,
                                            products.gender FROM visitors
                                            INNER JOIN buids on visitors.visitor_id = buids.visitor_id 
                                            INNER JOIN sessions on buids.buid = sessions.buid 
                                            INNER JOIN orders on sessions.session_id = orders.session_id 
                                            INNER JOIN products on orders.product_id = products.product_id 
                                            WHERE visitors.visitor_id = '{}'""".format(visitor_id['visitor_id']))
    id_list = list(get_highest_occurence(ordered))

    if len(id_list) == 0:
        viewed = search_sql(sql_connection, """SELECT distinct(viewed_before.product_id), products.category,products.sub_category,
                                            products.brand,products.gender FROM visitors   
                                            INNER JOIN viewed_before on visitors.visitor_id = viewed_before.visitor_id
                                            INNER JOIN products on viewed_before.product_id = products.product_id 
                                            INNER JOIN buids on visitors.visitor_id = buids.visitor_id 
                                            WHERE visitors.visitor_id = '{}'""".format(visitor_id['visitor_id']))
        id_list = list(get_highest_occurence(viewed))
    id_list = content_tree(sql_connection, id_list)
    return id_list

## functie voor het ophalen populaire / meest verkochte producten, staat op homepagina
def popular(sql_connection, mongo_db, visitor_id):
    personal_all = personal_transactions(sql_connection, visitor_id)
    popular_all = []
    popular_orders_last_2months = search_sql(sql_connection, """SELECT orders.product_id, COUNT(*) AS populair FROM sessions
                                                                INNER JOIN orders ON sessions.session_id = orders.session_id
                                                                WHERE sessions.session_start > CURRENT_DATE - INTERVAL '12 months'
                                                                GROUP BY orders.product_id ORDER BY populair DESC LIMIT 150""")
    popular_viewed_last_month = search_sql(sql_connection, """SELECT viewed_before.product_id FROM viewed_before
                                                              INNER JOIN visitors ON viewed_before.visitor_id = visitors.visitor_id
                                                              INNER JOIN buids ON visitors.visitor_id = buids.visitor_id
                                                              INNER JOIN sessions ON buids.buid = sessions.buid
                                                              WHERE sessions.session_start > CURRENT_DATE - INTERVAL '12 months'
                                                              GROUP BY viewed_before.product_id
                                                              ORDER BY COUNT(viewed_before.product_id) DESC LIMIT 10""")
    for tuple in popular_orders_last_2months:
        popular_all.append(tuple[0])
    for tuple in popular_viewed_last_month:
        popular_all.append(tuple[0])

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
    id_list = personal_transactions(sql_connection, visitor_id)
    return get_product_details(mongo_db, id_list, True)

## functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def collaborative(sql_db,mongo_db,sessiondata):
    id_list = []
    for product_id in sessiondata:
        query_results = search_sql(sql_db,"SELECT related, lift FROM lift_products WHERE product_id = '{}' ORDER BY lift DESC".format(product_id))
        for result in query_results:
	        id_list.append(result)
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
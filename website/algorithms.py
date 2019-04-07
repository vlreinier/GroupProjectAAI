from sql_commit_query import search_sql
from statistics import mode
from collections import Counter
import random


# haalt alternatieve producten op voor winkelwagentje a.d.h.v. lift en / of producteigenschappen
def alternatives(sql_db, sessiondata):
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
        query_results = search_sql(sql_db,
                                   "SELECT related, lift FROM lift_products WHERE product_id ='{}' ORDER BY lift DESC limit {}".format(
                                       product_id, limit))
        for result in query_results:
            id_list.append(result[0])
        if len(query_results) != limit:
            product_price = search_sql(sql_db,
                                       "SELECT selling_price FROM products WHERE product_id='{}'".format(product_id))
            limit_cat = limit - len(query_results)
            product_cat = search_sql(sql_db, "SELECT category FROM products WHERE product_id='{}'".format(product_id))
            query_results_cat = search_sql(sql_db,
                                           "SELECT product_id FROM products WHERE category='{}' AND selling_price BETWEEN {}*0.8 AND {}*1.2 ORDER BY RANDOM() LIMIT {}".format(
                                               product_cat[0][0], product_price, product_price, limit_cat))
            for result_cat in query_results_cat:
                id_list.append(result_cat[0])
    return id_list


# functie voor het ophalen van soortgelijke producten
def content_tree(sql_db, sessiondata):
    product_ids = []
    for product_id in sessiondata:
        query_results = search_sql(sql_db,
                                   "SELECT category, sub_category, sub_sub_category, selling_price, gender, brand FROM products WHERE product_id = '{}'".format(
                                       product_id))[0]
        category = query_results[0]
        sub_category = query_results[1]
        sub_sub_category = query_results[2]
        selling_price = query_results[3]
        gender = query_results[4]
        brand = query_results[5]
        query_results1 = search_sql(sql_db,
                                    "SELECT product_id FROM products WHERE category = '{}' AND sub_category = '{}' AND sub_sub_category = '{}' AND selling_price BETWEEN {} AND {} AND gender = '{}' AND brand = '{}' ORDER BY RANDOM() LIMIT 8".format(
                                        category, sub_category, sub_sub_category, int(selling_price) * 0.87,
                                                                                  int(selling_price) * 1.13, gender,
                                        brand))
        for result in query_results1:
            if result[0] != product_id:
                product_ids.append(result[0])
        if (len(query_results1) < 5) or ((len(product_ids) < 15) and (len(sessiondata) == 1)):
            query_results2 = search_sql(sql_db,
                                        "SELECT product_id FROM products WHERE category = '{}' AND sub_category = '{}' AND sub_sub_category = '{}' AND selling_price BETWEEN {} AND {} ORDER BY RANDOM() LIMIT 8".format(
                                            category, sub_category, sub_sub_category, int(selling_price) * 0.80,
                                                                                      int(selling_price) * 1.20))
            for result in query_results2:
                if result[0] != product_id:
                    product_ids.append(result[0])
            if len(query_results2) < 5:
                query_results3 = search_sql(sql_db,
                                            "SELECT product_id FROM products WHERE category = '{}' AND selling_price BETWEEN {} AND {} ORDER BY RANDOM() LIMIT 8".format(
                                                category, int(selling_price) * 0.80, int(selling_price) * 1.20))
                for result in query_results3:
                    if result[0] != product_id:
                        product_ids.append(result[0])
    return product_ids


# berekenen meest voorkomende producteigenschappen
def get_highest_occurence(ordered):
    new_list, product_ids, favourites, most_wanted = [], [], [], []
    sub_category, sub_sub_category, brand, gender = [], [], [], []

    if len(ordered) == 0:
        return new_list, favourites
    for i in ordered:
        product_ids.append(i[0])
        sub_category.append(i[1])
        sub_sub_category.append(i[2])
        brand.append(i[3])
        gender.append(i[4])
    counted_properties = Counter(sub_category) + Counter(sub_sub_category) + Counter(brand) + Counter(gender)
    counted_products = Counter(product_ids)

    for i in counted_products:
        if counted_products[i] > 2:
            favourites.append(i)

    for i in counted_properties:
        if counted_properties[i] > 2:
            most_wanted.append(i)
    if len(most_wanted) == 0:
        most_wanted = product_ids

    for i in ordered:
        for y in i:
            if y in most_wanted:
                new_list.append(i[0])

    return list(set(new_list)), favourites


# berekenen persoonlijke aanbeveling
def personal_preffered_products(sql_connection, visitor_id):
    if (visitor_id['visitor_id'] == '') or (visitor_id['visitor_id'] == None):
        return []
    ordered = search_sql(sql_connection, """SELECT orders.product_id, products.sub_category, 
                                            products.sub_sub_category, products.brand, products.gender FROM visitors
                                            INNER JOIN buids on visitors.visitor_id = buids.visitor_id 
                                            INNER JOIN sessions on buids.buid = sessions.buid 
                                            INNER JOIN orders on sessions.session_id = orders.session_id 
                                            INNER JOIN products on orders.product_id = products.product_id 
                                            WHERE visitors.visitor_id = '{}'""".format(visitor_id['visitor_id']))
    id_list, favourites = get_highest_occurence(ordered)
    if len(id_list) < 2:
        viewed = search_sql(sql_connection, """SELECT distinct(viewed_before.product_id), products.sub_category,
                                            products.sub_sub_category, products.brand,products.gender FROM visitors   
                                            INNER JOIN viewed_before on visitors.visitor_id = viewed_before.visitor_id
                                            INNER JOIN products on viewed_before.product_id = products.product_id 
                                            INNER JOIN buids on visitors.visitor_id = buids.visitor_id 
                                            WHERE visitors.visitor_id = '{}'""".format(visitor_id['visitor_id']))
        id_list, favourites = get_highest_occurence(viewed)
    id_list = content_tree(sql_connection, id_list + favourites)
    return id_list


# berekening populaire producten
def get_homepage_products(sql_connection, visitor_id):
    popular_all = []
    popular_orders_last_3months = search_sql(sql_connection, """SELECT orders.product_id FROM sessions
                                                                INNER JOIN orders ON sessions.session_id = orders.session_id
                                                                WHERE sessions.session_start > CURRENT_DATE - INTERVAL '3 months'
                                                                GROUP BY orders.product_id ORDER BY COUNT(*) DESC LIMIT 40""")
    for tuple in popular_orders_last_3months:
        popular_all.append(tuple[0])

    if len(popular_orders_last_3months) < 15:
        popular_viewed_last_3months = search_sql(sql_connection, """SELECT viewed_before.product_id FROM viewed_before
                                                                  INNER JOIN visitors ON viewed_before.visitor_id = visitors.visitor_id
                                                                  INNER JOIN buids ON visitors.visitor_id = buids.visitor_id
                                                                  INNER JOIN sessions ON buids.buid = sessions.buid
                                                                  WHERE sessions.session_start > CURRENT_DATE - INTERVAL '3 months'
                                                                  GROUP BY viewed_before.product_id
                                                                  ORDER BY COUNT(viewed_before.product_id) DESC LIMIT 40""")
        for tuple in popular_viewed_last_3months:
            popular_all.append(tuple[0])

    personal_all = personal_preffered_products(sql_connection, visitor_id)
    if len(personal_all) < 3:
        personal = random.sample(personal_all, len(personal_all))
        popular = random.sample(popular_all, 3 + (3 - len(personal_all)))
    else:
        personal = random.sample(personal_all, 3)
        popular = random.sample(popular_all, 3)
    return personal + popular
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
    elif len(sessiondata) == 3:
        limit = 2
    elif len(sessiondata) == 4:
        limit = 2
    else:
        limit = 1
    for product_id in sessiondata:
        results = []
        query_results = search_sql(sql_db,
                                   """SELECT distinct(lift_products.related), lift_products.lift FROM lift_products
                                        INNER JOIN products on lift_products.related = products.product_id
                                        WHERE lift_products.product_id ='{}' ORDER BY lift DESC limit {}""".format(product_id, limit))
        for result in query_results:
            if result[0] not in sessiondata:
                results.append(result[0])
        if len(results) != limit:
            limit_cat = limit - len(results)
            product_properties = search_sql(sql_db,
                                       "SELECT selling_price,category FROM products WHERE product_id='{}'".format(product_id))
            query_results_cat = search_sql(sql_db,
                                           "SELECT product_id FROM products WHERE category='{}' AND selling_price BETWEEN {}*0.87 AND {}*1.13 ORDER BY RANDOM() LIMIT {}".format(
                                               product_properties[0][1], product_properties[0][0], product_properties[0][0], limit_cat + 5))
            for result_cat in query_results_cat:
                if result_cat[0] not in sessiondata:
                    results.append(result_cat[0])
                    if len(results) == limit_cat:
                        break
        id_list = id_list + results
    return id_list


# functie voor het ophalen van soortgelijke producten
def content_tree(sql_db, sessiondata):
    product_ids = []
    for product_id in sessiondata:

        query_results = search_sql(sql_db,
                                   "SELECT category, sub_category, sub_sub_category, selling_price, gender, brand FROM products WHERE product_id = '{}'".format(
                                       product_id))[0]
        #producteigenschappen van query in dictionaries zetten
        category = query_results[0]
        sub_category = query_results[1]
        sub_sub_category = query_results[2]
        selling_price = query_results[3]
        gender = query_results[4]
        brand = query_results[5]
        #product_ids zoeken die dezelfde category, sub_category,sub_sub_category en prijs bevatten
        query_results1 = search_sql(sql_db,
                                    "SELECT product_id FROM products WHERE category = '{}' AND sub_category = '{}' AND sub_sub_category = '{}' AND selling_price BETWEEN {} AND {} AND gender = '{}' AND brand = '{}' ORDER BY RANDOM() LIMIT 8".format(
                                        category, sub_category, sub_sub_category, int(selling_price) * 0.87,
                                                                                  int(selling_price) * 1.13, gender,
                                        brand))
        for result in query_results1:
            if result[0] != product_id:
                product_ids.append(result[0])
        if (len(query_results1) < 5) or ((len(product_ids) < 15) and (len(sessiondata) == 1)): # bevat minder dan 5 producten in de resultaat van de query
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
    sub_sub_category, brand = [], []
    if len(ordered) == 0:
        return new_list, favourites
    for i in ordered:
        product_ids.append(i[0])
        sub_sub_category.append(i[1])
        brand.append(i[2])
    counted_properties = Counter(sub_sub_category) + Counter(brand)
    counted_products = Counter(product_ids)

    for i in counted_products:
        if counted_products[i] > 2:
            favourites.append(i)

    for i in counted_properties:
        if counted_properties[i] > 2:
            most_wanted.append(i)
    if len(most_wanted) < 2:
        most_wanted = product_ids

    for i in ordered:
        for y in i:
            if y in most_wanted:
                new_list.append(i[0])

    return list(set(new_list)), favourites


# berekenen persoonlijke aanbeveling
def personal_preffered_products(sql_connection, visitor_id):
    if (visitor_id['visitor_id'] == '') or (visitor_id['visitor_id'] is None):
        return []
    ordered = search_sql(sql_connection, """SELECT distinct(orders.product_id), 
                                            products.sub_sub_category, products.brand FROM visitors
                                            INNER JOIN buids on visitors.visitor_id = buids.visitor_id 
                                            INNER JOIN sessions on buids.buid = sessions.buid 
                                            INNER JOIN orders on sessions.session_id = orders.session_id 
                                            INNER JOIN products on orders.product_id = products.product_id
                                            WHERE visitors.visitor_id = '{}'""".format(visitor_id['visitor_id']))
    id_list, favourites = get_highest_occurence(ordered)
    if len(id_list) < 3:
        viewed = search_sql(sql_connection, """SELECT distinct(viewed_before.product_id),
                                            products.sub_sub_category, products.brand FROM visitors   
                                            INNER JOIN viewed_before on visitors.visitor_id = viewed_before.visitor_id
                                            INNER JOIN products on viewed_before.product_id = products.product_id 
                                            INNER JOIN buids on visitors.visitor_id = buids.visitor_id 
                                            WHERE visitors.visitor_id = '{}'""".format(visitor_id['visitor_id']))
        id_list, favourites = get_highest_occurence(viewed)
    id_list = content_tree(sql_connection, id_list + favourites)
    return id_list


# berekening populaire producten
def get_homepage_products(sql_connection, visitor_id, timespan):
    popular_all = []
    popular_orders_last_3months = search_sql(sql_connection, """SELECT orders.product_id FROM sessions
                                                                INNER JOIN orders ON sessions.session_id = orders.session_id
                                                                WHERE sessions.session_start > CURRENT_DATE - INTERVAL '{} months'
                                                                GROUP BY orders.product_id ORDER BY COUNT(*) DESC LIMIT 100""".format(timespan))
    for tuple in popular_orders_last_3months:
        popular_all.append(tuple[0])

    if len(popular_orders_last_3months) < 15:
        popular_viewed_last_3months = search_sql(sql_connection, """SELECT viewed_before.product_id FROM viewed_before
                                                                  INNER JOIN visitors ON viewed_before.visitor_id = visitors.visitor_id
                                                                  INNER JOIN buids ON visitors.visitor_id = buids.visitor_id
                                                                  INNER JOIN sessions ON buids.buid = sessions.buid
                                                                  WHERE sessions.session_start > CURRENT_DATE - INTERVAL '{} months'
                                                                  GROUP BY viewed_before.product_id
                                                                  ORDER BY COUNT(viewed_before.product_id) DESC LIMIT 40""".format(timespan))
        for tuple in popular_viewed_last_3months:
            popular_all.append(tuple[0])

    personal_all = personal_preffered_products(sql_connection, visitor_id)
    if len(personal_all) < 3:
        personal = personal_all
        popular = random.sample(popular_all, 3 + (3 - len(personal_all)))
    else:
        personal = random.sample(personal_all, 3)
        popular = random.sample(popular_all, 3)
    return personal + popular

# search bar
def similar_productnames(sql_connection, sessiondata):
    id_list = []
    if 'productname' in sessiondata:
        similar_named_products = search_sql(sql_connection, "SELECT products.product_id FROM products WHERE products.name ILIKE '%{0}%'".format(sessiondata['productname'])) # haal product_ids die de productname bevata
        for id in similar_named_products:
            id_list.append(id[0])
    if 'productid' in sessiondata:
        product_name = search_sql(sql_connection, "SELECT products.name FROM products WHERE product_id ='{}'".format(sessiondata['productid']))#haal uit producten die productname bevat als die van de ingevoerde productid
        product_name = product_name[0][0].split(' ')[0]
        similar_id_products = search_sql(sql_connection, "SELECT product_id FROM products WHERE products.name ILIKE '%{0}%'".format(product_name))
        id_list.append(sessiondata['productid'])
        for id in similar_id_products:
            id_list.append(id[0])
    return id_list


def season_products(sql_connection,sessiondata):
    qry="SELECT tb1.product_id,aantal_in_orders, aantal_in_seizoen,(CAST(aantal_in_seizoen AS float)/CAST(aantal_in_orders AS float)) as season_popularity FROM( " \
        "SELECT product_id,count(product_id) as aantal_in_orders" \
        "FROM orders" \
        "where product_id in" \
        "	(select distinct product_id  from orders" \
        "inner join sessions on sessions.session_id=orders.session_id" \
        "where sessions.session_start>(current_date-interval'6 months')" \
        "and sessions.session_start<(current_date-interval'3 months'))" \
        "group by product_id" \
        "order by aantal_in_orders DESC" \
        ") AS tb1" \
        "INNER JOIN (SELECT product_id,count(product_id) as aantal_in_seizoen" \
        "FROM (select product_id  from orders" \
        "inner join sessions on sessions.session_id=orders.session_id" \
        "where sessions.session_start>(current_date-interval'6 months')" \
        "and sessions.session_start<(current_date-interval'3 months')) as seizoens_aankopen" \
        "GROUP BY product_id" \
        "ORDER BY aantal_in_seizoen DESC) as tb2 on tb2.product_id=tb1.product_id" \
        "ORDER BY season_popularity DESC" \
        "LIMIT 8"
    s_product=search_sql(sql_connection,qry)

#tijdsinterval berkenen
def calculate_timespan(sql_connection,grens_in_percentage):

    qry_aantal_orders="""SELECT count(orders.product_id) FROM orders INNER JOIN sessions on sessions.session_id=orders.session_id 
                        WHERE sessions.session_start>(current_date-interval'12 months')"""
    aantal_orders=search_sql(sql_connection,qry_aantal_orders)[0][0]

    begintime = search_sql(sql_connection, "SELECT session_start FROM sessions ORDER BY session_start ASC  LIMIT 1")[0][0]
    endtime = search_sql(sql_connection, "SELECT session_start FROM sessions ORDER BY session_start DESC LIMIT 1")[0][0]
    dataset_timespan = ((endtime - begintime).days) // 30

    for interval in [1,2,3,6,12]:
        timespan = interval
        amount_of_products=[]
        mean = 0
        for maanden_geleden in range(0,dataset_timespan,interval):
            if maanden_geleden+(0.5*interval)>dataset_timespan:
                continue
            qry="""SELECT count(orders.product_id)
                   FROM orders
                   INNER JOIN sessions on sessions.session_id=orders.session_id
                   WHERE sessions.session_start>(current_date-interval'{} months')
                   AND sessions.session_start<(current_date-interval'{} months')""".format(str(maanden_geleden+interval),str(maanden_geleden))
            data=search_sql(sql_connection,qry)
            amount_of_products.append(data[0][0])
        mean = sum(amount_of_products)/len(amount_of_products)

        if (mean/aantal_orders)*100>grens_in_percentage:
            break

    return timespan


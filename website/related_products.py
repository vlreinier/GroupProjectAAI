from sql_commit_query import search_sql
from statistics import mode

## functie voor het ophalen van soortgelijke producten
def content_tree(sql_db, sessiondata):
	product_ids = []
	for product_id in sessiondata:
		query_results = search_sql(sql_db, "SELECT category, sub_category, sub_sub_category, selling_price, gender, brand FROM products WHERE product_id = '{}'".format(product_id))[0]
		category = query_results[0]
		sub_category = query_results[1]
		sub_sub_category = query_results[2]
		selling_price = query_results[3]
		gender = query_results[4]
		brand = query_results[5]
		
		query_results1 = search_sql(sql_db, "SELECT product_id FROM products WHERE category = '{}' AND sub_category = '{}' AND sub_sub_category = '{}' AND selling_price BETWEEN {} AND {} AND gender = '{}' AND brand = '{}' ORDER BY RANDOM() LIMIT 8".format(category, sub_category, sub_sub_category, int(selling_price) * 0.87, int(selling_price) * 1.13, gender,brand))
		for result in query_results1:
			if result[0] != product_id:
				product_ids.append(result[0])
		if (len(query_results1) < 5) or ((len(product_ids) < 15) and (len(sessiondata) == 1)):
			query_results2 = search_sql(sql_db, "SELECT product_id FROM products WHERE category = '{}' AND sub_category = '{}' AND sub_sub_category = '{}' AND selling_price BETWEEN {} AND {} ORDER BY RANDOM() LIMIT 8".format(category, sub_category, sub_sub_category, int(selling_price) * 0.80, int(selling_price) * 1.20))
			for result in query_results2:
				if result[0] != product_id:
					product_ids.append(result[0])
			if len(query_results2) < 5:
				query_results3 = search_sql(sql_db, "SELECT product_id FROM products WHERE category = '{}' AND selling_price BETWEEN {} AND {} ORDER BY RANDOM() LIMIT 8".format(category, int(selling_price) * 0.80, int(selling_price) * 1.20))
				for result in query_results3:
					if result[0] != product_id:
						product_ids.append(result[0])
	return product_ids

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

def personal_preffered_products(sql_connection, visitor_id):
    if visitor_id['visitor_id'] == '':
        return []
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

def get_popular_products(sql_connection, visitor_id):
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
    return popular_all
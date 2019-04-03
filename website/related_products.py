from sql_commit_query import search_sql

## functie voor het ophalen van soortgelijke producten
def content_tree(sql_db, sessiondata):
	product_ids = []
	for product_id in sessiondata:
		query_results = search_sql(sql_db, "SELECT category, sub_category, sub_sub_category, selling_price, gender, brand FROM products WHERE product_id = '{}'".format(sessiondata[product_id]))[0]
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
from sql_functions import search_sql
		
def merge_nested_dictvalues(startdict, columns):
	for key, value in list(startdict.items()):
		if isinstance(value,dict):
			for k,v in value.items():
				if k in columns:
					startdict[k] = v
	return startdict
		
def resolve_errors(startdict, columns):
	for file in startdict:
		file = merge_nested_dictvalues(file, columns)
		for column in columns:
			if not column in file:
				file[column] = str(None)
			else:
				if type(file[column]) == str:
					file[column] = file[column].replace("\\","").replace("'","").replace("\"","")
				if file[column] == None:
					file[column] = str(None)
	return startdict

def insert_products(products, sql_connection, inserts):
	products_columns = ['_id','name','doelgroep','brand','gender','category','sub_category','sub_sub_category','selling_price','availability']
	products = resolve_errors(products, products_columns)
	for i in products:
		if ((i['selling_price'] == 'None') and (i['availability'] == 'None')) or (type(i['category']) == list):
			continue
		inserts+="INSERT INTO products Values('{}','{}','{}','{}','{}','{}','{}','{}',{},'{}');\n".format(i['_id'],i['name'],i['brand'],i['gender'],i['doelgroep'],i['category'],i['sub_category'],i['sub_sub_category'],i['selling_price'],i['availability'])
	return inserts

def insert_visitors(visitors, sql_connection, inserts):
	visitors_columns = ['_id']
	visitors = resolve_errors(visitors, visitors_columns)
	for i in visitors:
		inserts+="INSERT INTO visitors Values('{}');\n".format(i['_id'])
	return inserts
	
def insert_previously_recommended(previously_recommended, sql_connection, inserts):
	products = set()
	previously_recommended_columns = ['_id','previously_recommended']
	previously_recommended = resolve_errors(previously_recommended, previously_recommended_columns)
	for id in search_sql(sql_connection, "SELECT product_id FROM products"):
		products.add(str(id[0]))
	for i in previously_recommended:
		if i['previously_recommended'] != 'None':
			for product_id in i['previously_recommended']:
				if product_id in products:
					inserts+="INSERT INTO previously_recommended Values('{}','{}');\n".format(str(i['_id']), product_id)
	return inserts
	
def insert_viewed_before(viewed_before, sql_connection, inserts):
	products = set()
	viewed_before_columns = ['_id','viewed_before']
	viewed_before = resolve_errors(viewed_before, viewed_before_columns)
	for id in search_sql(sql_connection, "SELECT product_id FROM products"):
		products.add(str(id[0]))
	for i in viewed_before:
		if i['viewed_before'] != 'None':
			for product_id in i['viewed_before']:
				if product_id in products:
					inserts+="INSERT INTO viewed_before Values('{}','{}');\n".format(str(i['_id']), product_id)
	return inserts
	
def insert_buids(buids, sql_connection, inserts):
	buids_sql = set()
	buids_columns = ['_id','buids']
	buids = resolve_errors(buids, buids_columns)
	for buid in search_sql(sql_connection, "SELECT buid FROM buids"):
		buids_sql.add(str(buid[0]))
	for i in buids:
		if i['buids'] != 'None':
			for buid in i['buids']:
				if not buid in buids_sql:
					inserts+="INSERT INTO buids Values('{}','{}');\n".format(str(i['_id']), buid)
					buids_sql.add(buid)
	return inserts
	
def insert_sessions(sessions, sql_connection, inserts):
	buids = set()
	sessions_orders = set()
	sessions_columns = ['_id', 'buid','session_start','session_end']
	sessions = resolve_errors(sessions, sessions_columns)
	for buid in search_sql(sql_connection, "SELECT buid FROM buids"):
		buids.add(str(buid[0]))
	for session in search_sql(sql_connection, "SELECT session_id FROM orders"):
		sessions_orders.add(str(session[0]))
	for i in sessions:
		if type(i['buid']) == list:
			if type(i['buid'][0]) == list:
				i['buid'][0] = i['buid'][0][0]
			i['buid'] = i['buid'][0]
		if (i['_id'] in sessions_orders) and (i['buid'] in buids):
			inserts+="INSERT INTO sessions Values('{}','{}','{}','{}');\n".format(str(i['_id']), str(i['buid']),i['session_start'], i['session_end'])
	return inserts
	
def insert_orders(orders, sql_connection, inserts):
	products = set()
	orders_columns = ['_id','order']
	orders = resolve_errors(orders, orders_columns)
	for id in search_sql(sql_connection, "SELECT product_id FROM products"):
		products.add(str(id[0]))
	for i in orders:
		if i['order'] != 'None':
			if (type(i['order']) == dict) and (i['order'] != {}):
				for product_id in i['order']['products']:
					if product_id['id'] in products:
						inserts+="INSERT INTO orders Values('{}','{}');\n".format(str(i['_id']), product_id['id'])
	return inserts
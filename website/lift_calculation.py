from sql_commit_query import search_sql, commit_sql
import time
import datetime
import sys


# functie voor het maken van een SQL tabel voor lift productcombinaties
def lift_table(sql_db):
    query = (
        """
	DROP TABLE IF EXISTS lift_products CASCADE;
	
	CREATE TABLE lift_products (
	product_id VARCHAR(255) NOT NULL,
	related VARCHAR(255) NOT NULL,
	lift FLOAT NOT NULL );
	
	ALTER TABLE lift_products
		ADD FOREIGN KEY (product_id) REFERENCES products(product_id),
		ADD FOREIGN KEY (related) REFERENCES products(product_id);
	""")
    commit_sql(sql_db, query)


# functie voor het ophalen totaal aantal transacties a.d.h.v. SQL query
def total_transactions(sql_db, query):
    query_results = search_sql(sql_db, query)[0][0]
    return query_results


# functie voor het uitrekenen van support per product a.d.h.v. SQL query en totaal aantal transacties
def calculate_support(sql_db, total_transactions, query):
    supports = {}
    query_results = search_sql(sql_db, query)
    for result in query_results:
        product_id = result[0]
        support = result[1] / total_transactions
        supports[product_id] = support
    return supports


# functie voor het berekenen van lift voor product x met y, uit orders
# elk product moet 1 op de 10000 keer voorkomen anders is de aanbeveling niet per se een goede aanbeveling
def lift_orders(sql_db):
    starttime = time.time()
    total_orders = total_transactions(sql_db, "SELECT count(distinct(session_id)) FROM orders")
    support_orders = calculate_support(sql_db, total_orders,
                                       "SELECT product_id, count(distinct(session_id)) FROM orders GROUP BY product_id")

    for product_x, support_x in support_orders.items():
        query_results = search_sql(sql_db,
                                   "SELECT product_id, COUNT(DISTINCT(session_id)) AS aantal FROM orders WHERE session_id IN"
                                   "(SELECT DISTINCT(session_id) FROM orders WHERE product_id = '{}') AND product_id != '{}'"
                                   "GROUP BY product_id ORDER BY aantal DESC LIMIT 15".format(product_x, product_x))
        for result in query_results:
            product_y = result[0]
            xy_together = result[1]
            support_y = support_orders[product_y]
            support_xy = xy_together / total_orders
            lift_xy = support_xy / (support_x * support_y)
            if lift_xy > 5 and support_x > 0.0001 and support_y > 0.0001:
                insert = [product_x, product_y, lift_xy]
                commit_sql(sql_db, "INSERT INTO lift_products VALUES{}".format(tuple(insert)))
    sql_db.commit()
    print('lift orders runtime:', (time.time() - starttime) / 60)


# functie voor het beheren van gekozen lift berekeningen, viewed before is verwijderd
def lift(sql_db):
    print("Lift insertion is started at ", datetime.datetime.now())
    lift_table(sql_db)
    lift_orders(sql_db)
    print("Lift insertion is ended at ", datetime.datetime.now())

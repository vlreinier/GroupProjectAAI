from generate_product_details import get_product_details
from algorithms import content_tree, get_popular_products, personal_preffered_products, alternatives
import random


# functie voor het ophalen populaire icm persoonlijke producten, staat op homepagina
def homepage(sql_connection, mongo_db, visitor_id):
    personal_all = personal_preffered_products(sql_connection, visitor_id)
    popular_all = get_popular_products(sql_connection, visitor_id)
    get_personal = len(personal_all)
    get_popular = len(popular_all)

    if get_personal < 3 and get_popular >= get_popular + (3 - get_personal):
        get_popular = get_popular + (3 - get_personal)
    if get_popular < 3 and get_personal >= get_personal + (3 - get_popular):
        get_personal = get_personal + (3 - get_popular)
    if get_popular > 2 and get_personal > 2:
        get_popular = 3
        get_personal = 3

    personal = random.sample(personal_all, get_personal)
    popular = random.sample(popular_all, get_popular)
    return get_product_details(mongo_db, personal + popular, True)


# functie voor het ophalen van persoonlijke aanbevelingen bezoekersid a.d.h.v. eerder bekeken en gelijke producten
def personal(sql_connection, mongo_db, visitor_id):
    id_list = personal_preffered_products(sql_connection, visitor_id)
    return get_product_details(mongo_db, id_list, True)


# functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def collaborative(sql_db, mongo_db, sessiondata):
    id_list = alternatives(sql_db, sessiondata)
    return get_product_details(mongo_db, id_list, True)

# laad opgeslagen producten in winkelwagen
def shoppingcart(sql_db, mongo_db, sessiondata):
    id_list = []
    for id in sessiondata:
        id_list.append(str(id))
    return get_product_details(mongo_db, id_list, False)

# laad aangeklikt product op similar page
def loadselected(sql_db, mongo_db, sessiondata):
    id_list = []
    for id in sessiondata:
        id_list.append(str(sessiondata[id]))
    return get_product_details(mongo_db, id_list, False)


# functie voor het ophalen van soortgelijk product aanbevelingen a.d.h.v. aangeklikt product
def selectedsimilar(sql_db, mongo_db, sessiondata):
    id_list = []
    for i in sessiondata:
        id_list.append(sessiondata[i])
    id_list = content_tree(sql_db, id_list)
    return get_product_details(mongo_db, id_list, False)

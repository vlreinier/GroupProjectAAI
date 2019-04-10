from generate_product_details import get_product_details
from algorithms import content_tree, get_homepage_products, personal_preffered_products, alternatives, similar_productnames


# functie voor het ophalen populaire icm persoonlijke producten, staat op homepagina
def homepage(sql_connection, mongo_db, visitor_id, timespan):
    id_list = get_homepage_products(sql_connection, visitor_id, timespan)
    return get_product_details(mongo_db, id_list, True, 6)


# functie voor het ophalen van persoonlijke aanbevelingen bezoekersid a.d.h.v. eerder bekeken en gelijke producten
def personal(sql_connection, mongo_db, visitor_id):
    id_list = personal_preffered_products(sql_connection, visitor_id)
    return get_product_details(mongo_db, id_list, True, 6)


# functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def collaborative(sql_db, mongo_db, sessiondata):
    id_list = alternatives(sql_db, sessiondata)
    return get_product_details(mongo_db, id_list, True, 6)


# laad opgeslagen producten in winkelwagen
def shoppingcart(sql_db, mongo_db, sessiondata):
    id_list = []
    for id in sessiondata:
        id_list.append(str(id))
    return get_product_details(mongo_db, id_list, False, 0)


# laad aangeklikt product op similar page
def loadselected(sql_db, mongo_db, sessiondata):
    id_list = []
    for id in sessiondata:
        id_list.append(str(sessiondata[id]))
    return get_product_details(mongo_db, id_list, False, 0)


# functie voor het ophalen van soortgelijk product aanbevelingen a.d.h.v. aangeklikt product
def selectedsimilar(sql_db, mongo_db, sessiondata):
    id_list = []
    for i in sessiondata:
        id_list.append(sessiondata[i])
    id_list = content_tree(sql_db, id_list)
    return get_product_details(mongo_db, id_list, False, 10)


# functie voor het ophalen van klantgedrag aanbevelingen a.d.h.v. opgeslagen producten
def search_on_name(sql_db, mongo_db, sessiondata):
    id_list = similar_productnames(sql_db, sessiondata)
    return get_product_details(mongo_db, id_list, False, 80)
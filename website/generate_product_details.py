import random


# functie voor ophalen product eigenschappen a.d.h.v. product id's en opslaan in dictionary's in 1 lijst
def get_product_details(mongo_db, id_list, shuffle, maximum):
    all_dict = []
    count = 0
    seen = set()
    if shuffle:
        random.shuffle(id_list)

    for product_id in id_list:
        product = mongo_db.products.find_one({'_id': product_id})

        try:
            if product_id not in seen:
                count += 1
                dict = {}
                seen.add(product_id)
                dict['image'] = product['images'][0][0]
                if dict['image'] == None:
                    dict['image'] = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
                dict['name'] = product['name']
                dict['price'] = '€' + str(product['price']['selling_price'])[:-2] + ',' + str(
                    product['price']['selling_price'])[-2:]
                if int(product['price']['selling_price']) < 100:
                    dict['price'] = '€' + '0' + str(product['price']['selling_price'])[:-2] + ',' + str(
                        product['price']['selling_price'])[-2:]
                dict['availability'] = product['properties']['availability']
                dict['brand'] = product['brand']
                dict['category'] = product['category']
                dict['_id'] = str(product_id)
                all_dict.append(dict)
                if maximum != 0 and count == maximum:
                    return all_dict

        except Exception:
            count -= 1
            continue
    return all_dict

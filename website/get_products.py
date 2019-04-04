import random

## functie voor ophalen product eigenschappen a.d.h.v. product id's en opslaan in dictionary's in 1 lijst
def get_product_details(mongo_db, id_list, shuffle):
	all_dict = []
	count = 0
	seen = set()
	if shuffle == True:
		random.shuffle(id_list)
	
	for product_id in id_list:
		product = mongo_db.products.find_one({'_id':product_id})
		
		try:
			if product_id not in seen:
				dict = {}
				seen.add(product_id)
				dict['image'] = product['images'][0][0]
				dict['name'] = product['name']
				dict['price'] = '€' + str(product['price']['selling_price'])[:-2] + ',' + str(product['price']['selling_price'])[-2:]
				if int(product['price']['selling_price']) < 100:
					dict['price'] = '€'+'0' + str(product['price']['selling_price'])[:-2] + ',' + str(
						product['price']['selling_price'])[-2:]
				dict['availability'] = product['properties']['availability']
				dict['brand'] = product['brand']
				dict['category'] = product['category']
				dict['_id'] = str(product_id)
				all_dict.append(dict)
				if count == 4:
					return all_dict
				count+=1
				
		except Exception:
			continue
		
	return all_dict
from analyse import MongoDB
import operator

data_list_products=MongoDB.get_data('products',100)
data_list_sessions=MongoDB.get_data('sessions',100)
data_list_profiles=MongoDB.get_data('visitors',300)

total_count_products=MongoDB.count_value('products')
total_count_sessions=MongoDB.count_value('sessions')
total_count_visitors=MongoDB.count_value('visitors')

def analyse_data(coll,att):
    dictionary={}
    exist=total_count_products - MongoDB.count_value(coll,{att:None})
    dictionary['exist']=exist
    distinct = MongoDB.distinct_values(coll, att)
    for value in distinct:
        count = MongoDB.count_value(coll, {att: value})
        dictionary[value]=count
    dictionary['distinct']=distinct
    return dictionary

dubbele=[]
no_order_products=0
no_order=0
data_count=0
for i in data_list_sessions:
    data_count+=1
    if 'order' in i:
        list1=[]
        if 'products' in i['order']:
            for j in i['order']['products']:
                if j in list1:
                    dubbele.append(i)
                list1.append(j)
        else:
            no_order_products+=1
            #print(i['order'])
    else:
        no_order+=1

print(data_count)
print(no_order,no_order_products)


category=analyse_data('products','category')
sub_category=analyse_data('products','sub_category')
sub_sub_category=analyse_data('products','sub_sub_category')
sub_sub_sub_category=analyse_data('products','sub_sub_sub_category')
herhaalaankopen=analyse_data('products','herhaalaankopen')
fast_mover=analyse_data('products','fast_mover')
flavor=analyse_data('products','flavor')
gender=analyse_data('products','gender')
size=analyse_data('products','size')
predict_out_of_stock=analyse_data('product','predict_out_of_stock')


print(herhaalaankopen)
print(fast_mover)
print(flavor)
print(gender)
print(sub_category)
print(sub_sub_category)
print(sub_sub_sub_category)
print(size)
print('predict_out_of_stock:',predict_out_of_stock)

count=0
count2=0
for i in data_list_sessions:
    if 'events' in i:
        for j in i['events']:
            count2+=1
            if 'product' in j:
                if j['product']!=None:
                    count+=1
events_products={'exist in %':100*count/count2}

omzet={}
count=0
for i in data_list_sessions:
    if 'order' in i:
        for j in i['order']['products']:
            price=data_list_products[count]['price']['selling_price']
            id=j['id']
            if id not in omzet:
                omzet[id]=1
            else:
                omzet[id]+=1
    count+=1



count3=0
count=0
count2=0
a=0
b=[]
for i in data_list_products:
    count+=1
    if 'properties' in i:
        if 'doelgroep' in i['properties']:
            if i['properties']['doelgroep'] not in b:
                b.append(i['properties']['doelgroep'])
                a+=1
            count2+=1
            if i['properties']['doelgroep']!=None:
                count3+=1

doelgroep={'exist in %':100*count3/count,'distinct:':b}

count=0
count2=0
amount_of_pr=0
for i in data_list_profiles:
    count+=1
    if 'previously_recommended' in i:
        if i['previously_recommended']!=None:
            count2+=1
            amount_of_pr+=len(i['previously_recommended'])

previously_recommended_products={'exist in %':100*count2/count,'average amount of products':amount_of_pr/count2}
print(previously_recommended_products)




print(doelgroep)
print(events_products)
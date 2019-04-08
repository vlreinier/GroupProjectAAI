from analyse import MongoDB
import operator
import psycopg2

data_list_products=MongoDB.get_data('products',100)
data_list_sessions=MongoDB.get_data('sessions',100)
data_list_profiles=MongoDB.get_data('visitors',300)

total_count_products=MongoDB.count_value('products')
total_count_sessions=MongoDB.count_value('sessions')
total_count_visitors=MongoDB.count_value('visitors')




sql_db = psycopg2.connect("dbname={} user={} password={}".format('voordeelshop', 'postgres', 'Tom-1998'))


local_list=[]
change_dict={}
for dag in range(1,12):
    change=0
    dag2=dag+1
    if dag<10:
        if dag2<10:
            dag2='0'+str(dag2)
        dag='0'+str(dag)
    else:
        dag2=str(dag2)
        dag=str(dag)
    qry="select product_id, count( orders.product_id) as aantal from orders " \
        "inner join sessions on sessions.session_id=orders.session_id " \
        "where sessions.session_start>'2018-01-{} 15:40:46.619000' and sessions.session_start<'2018-02-{} 15:40:46.619000' " \
        "group by orders.product_id " \
        "order by aantal DESC limit 6".format(dag,dag2)

    cursor=sql_db.cursor()
    cursor.execute(qry)
    data=cursor.fetchall()
    print('dag ',dag)
    print(qry)
    print(data)

    if dag==1:
        for i in data:
            local_list.append(i[0])
    else:
        for i in data:
            if i[0] not in local_list:
                change=1
            local_list.append(i[0])
    if change:
        change_dict[dag]='changed'
    else:
        change_dict[dag]='same'
print(change_dict)


#
#
# def analyse_data(coll,att):
#     dictionary={}
#     exist=total_count_products - MongoDB.count_value(coll,{att:None})
#     dictionary['exist']=exist
#     distinct = MongoDB.distinct_values(coll, att)
#     for value in distinct:
#         count = MongoDB.count_value(coll, {att: value})
#         dictionary[value]=count
#     dictionary['distinct']=distinct
#     return dictionary
#
# dubbele=[]
# no_order_products=0
# no_order=0
# data_count=0
# for i in data_list_sessions:
#     data_count+=1
#     if 'order' in i:
#         list1=[]
#         if 'products' in i['order']:
#             for j in i['order']['products']:
#                 if j in list1:
#                     dubbele.append(i)
#                 list1.append(j)
#         else:
#             no_order_products+=1
#             #print(i['order'])
#     else:
#         no_order+=1
#
# print(data_count)
# print(no_order,no_order_products)
#
#
# category=analyse_data('products','category')
# sub_category=analyse_data('products','sub_category')
# sub_sub_category=analyse_data('products','sub_sub_category')
# sub_sub_sub_category=analyse_data('products','sub_sub_sub_category')
# herhaalaankopen=analyse_data('products','herhaalaankopen')
# fast_mover=analyse_data('products','fast_mover')
# flavor=analyse_data('products','flavor')
# gender=analyse_data('products','gender')
# size=analyse_data('products','size')
# predict_out_of_stock=analyse_data('product','predict_out_of_stock')
#
#
# print(herhaalaankopen)
# print(fast_mover)
# print(flavor)
# print(gender)
# print(sub_category)
# print(sub_sub_category)
# print(sub_sub_sub_category)
# print(size)
# print('predict_out_of_stock:',predict_out_of_stock)
#
# count=0
# count2=0
# for i in data_list_sessions:
#     if 'events' in i:
#         for j in i['events']:
#             count2+=1
#             if 'product' in j:
#                 if j['product']!=None:
#                     count+=1
# events_products={'exist in %':100*count/count2}
#
# omzet={}
# count=0
# for i in data_list_sessions:
#     if 'order' in i:
#         for j in i['order']['products']:
#             price=data_list_products[count]['price']['selling_price']
#             id=j['id']
#             if id not in omzet:
#                 omzet[id]=1
#             else:
#                 omzet[id]+=1
#     count+=1
#
#
#
# count3=0
# count=0
# count2=0
# a=0
# b=[]
# for i in data_list_products:
#     count+=1
#     if 'properties' in i:
#         if 'doelgroep' in i['properties']:
#             if i['properties']['doelgroep'] not in b:
#                 b.append(i['properties']['doelgroep'])
#                 a+=1
#             count2+=1
#             if i['properties']['doelgroep']!=None:
#                 count3+=1
#
# doelgroep={'exist in %':100*count3/count,'distinct:':b}
#
# count=0
# count2=0
# amount_of_pr=0
# for i in data_list_profiles:
#     count+=1
#     if 'previously_recommended' in i:
#         if i['previously_recommended']!=None:
#             count2+=1
#             amount_of_pr+=len(i['previously_recommended'])
#
# previously_recommended_products={'exist in %':100*count2/count,'average amount of products':amount_of_pr/count2}
# print(previously_recommended_products)
#
#
#
#
# print(doelgroep)
# print(events_products)
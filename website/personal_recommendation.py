import psycopg2
import pymongo
from website.database_connections import  connect_sql

#functie om te zien of een bepaalde klant heeft iets gekocht of bekeken
def check_if(visitor_id) :
    'Ditionaries met queries'
    queries_controle = dict1= {#o = Bij een bepaalde visitor_id, wordt gezien hoeveel heeft hij/zij gekocht
        'or':'SELECT orders.product_id, products.category,products.sub_category, products.brand, products.gender '
            'FROM visitors '
            'INNER JOIN buids on visitors.visitor_id = buids.visitor_id '
            'INNER JOIN sessions on buids.buid = sessions.buid '
            'INNER JOIN orders on sessions.session_id = orders.session_id '
            'INNER JOIN products on orders.product_id = products.product_id '
            'WHERE visitors.visitor_id = \'{}\''.format(visitor_id),
        #vb= bij een bepaalde visistor_id wordt gezien hoeveel heeft hij/zij eerdere bekeken
        'vb':'SELECT vb.product_id,p.category,p.sub_category,p.brand,p.gender,Count(*) ' 
            'from Viewed_before as vb,Visitors as v, Products as p '
            'group by v.visitor_id,vb.product_id,p.name,p.gender, p.category,p.product_id '
            'Having count(*)>= 1 AND p.product_id = vb.product_id '
            'AND v.visitor_id = \'{}\''.format(visitor_id)
    };
    return queries_controle

def q_or(dbname, dbuser, dbpass,visitor_id):
    conn = connect_sql(dbname, dbuser, dbpass)
    cur = conn.cursor()
    q = check_if(visitor_id)
    cur.execute(q['or'])
    o = cur.fetchall()
    cur.close()
    return o

def q_vb(dbname, dbuser, dbpass,visitor_id):
    conn = connect_sql(dbname, dbuser, dbpass)
    cur = conn.cursor()
    q = check_if(visitor_id)
    cur.execute(q['vb'])
    vb = cur.fetchall()
    cur.close()
    return vb


def check_o_vb(visitor_id,dbname, dbuser, dbpass):
    'Controller of een klant heeft iets  gekocht'
    o=  q_or(dbname, dbuser, dbpass,visitor_id,)
    vb =q_vb(dbname, dbuser, dbpass,visitor_id)

    if len(o)>=1: #order
       m,c,g = com_orders(o,visitor_id,dbname, dbuser, dbpass)
       return m,c,g
    elif len(vb)>=1: #eerdere bekeken
        m,c,g = com_orders(vb,visitor_id,dbname, dbuser, dbpass,)
        return m,c,g
    else:
        print('niks gekocht/bekeken')


def com_orders(result_query,visitor_id,dbname, dbuser, dbpass):
    'Product information vergelijken met elkaar en return een ideale product'
    conn = connect_sql(dbname, dbuser, dbpass)
    cur = conn.cursor()
    m,c,g = [],[],[]
    n= 0
    while n<=10:
        if result_query[n][1] == result_query[n+1][1]:
            m.append(result_query[n][1])
            n=+1
        if result_query[n][2] == result_query[n + 1][2]:
            c.append(result_query[n][2])
            n = +1
        if result_query[n][3] == result_query[n + 1][3]:
            g.append(result_query[n][3])
            n = +1
    return m,c,g

#test
visitor_id,dbname, dbuser, dbpass = '59dce8c1a56ac6edb4cf22e8', 'voordeelshop', 'postgres','amaryllis'
print(check_o_vb(visitor_id,dbname, dbuser, dbpass ))

#def ip_orders(m,c,g,result_query,visitor_id):
 #   'Bepaalt wie het meest voorkomt in de lijsten vna vergeleken producteninformatie'
  #  m,c,g =com_orders(result_query,visitor_id)

#----------------------------------------------------------------------------------------------------------------------------------
#dict = {'test':'Select * from products Limit 5'}
#dbname,dbuser,dbpass = 'voordeelshop2', 'postgres','amaryllis'
#def test(dbname,dbuser,dbpass, dict):
 #   conn = connect_sql(dbname, dbuser, dbpass)
 #   cur = conn.cursor()
 #   dict = {'test': 'Select * from Visitors Limit 5'}
 #   cur.execute(dict['test'])
 #   fetched = cur.fetchall()
 #   print(fetched)
        #print(i)

#test(dbname,dbuser,dbpass, dict)


#def check_if(dbname, dbuser, dbpassword, visitor_id):
#    lst_id = []
#    dt= dict_query(visitor_id)
#    connect = psycopg2.connect("dbname={} user={} password={}".format(dbname, dbuser, dbpassword)) # connect to database
#    cur = connect.cursor()
#    if (dt.dict1['o']>=1)== True:
#        print(dt.dict2['order'])

# 1. query die de productinformkrijgen van de gekochte product.

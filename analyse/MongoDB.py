import psycopg2
import random
from pymongo import MongoClient

def get_database(coll,limiet, query={}):
    client = MongoClient('mongodb://localhost:27017')
    db = client['voordeelshop']
    collection_student = db[coll]
    data = collection_student.find(query).limit(limiet)
    return data

def count_value(coll,query={}):
    client = MongoClient('mongodb://localhost:27017')
    db = client['voordeelshop']
    collection_student = db[coll]
    data = collection_student.find(query).count()
    return data

def distinct_values(coll,query={}):
    client = MongoClient('mongodb://localhost:27017')
    db = client['voordeelshop']
    collection_student = db[coll]
    data = collection_student.distinct(query)
    return data

def get_data(coll,limiet):
    data=get_database(coll,limiet)
    data_list=[]
    for datapoint in data:
        data_list.append(datapoint)
    return data_list
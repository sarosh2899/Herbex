
from pymongo import MongoClient

def create_connection_to_mongodb(connection_string):
    print('conection ding')
    
    client = MongoClient(connection_string)
    return client

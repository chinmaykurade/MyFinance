import os

from pymongo import MongoClient
client = MongoClient(os.environ.get('MONGO_URI'))

db = client.STOCKS

for i, company in enumerate(db.stocks_data.find()):
    print(company,'\n')

clist = list(db.stocks_data.find())


import pymongo
import csv

connection = pymongo.MongoClient("localhost", 27017)
db = connection.testDB
co = db.Tokens

db.drop_collection("Tokens")

f = open('token_data.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    key, valueArr = line[0].split(':')
    values = valueArr.split('/')

    if values[0] is not '':
        data['token'] = dict({key: values})
        co.insert_one(data)
f.close()
import pymongo
import csv

connection = pymongo.MongoClient("localhost", 27017)
db = connection.testDB

for i in range(1, 7):
    collectionName = "Slot" + str(i)
    co = db[collectionName]
    db.drop_collection(collectionName)
    f = open('slot'+str(i)+'.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)
    for line in rdr:
        data = {}
        for num in range(len(line)):
            if num % 2 == 0:
                data[line[num]] = line[num + 1]
        co.insert(data)
    f.close()

db.drop_collection("Data")
co = db.Data
f = open('data.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()


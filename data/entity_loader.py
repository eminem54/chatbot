import pymongo
import csv

connection = pymongo.MongoClient("localhost", 27017)
db = connection.testDB

<<<<<<< HEAD
db.drop_collection("Slot1")
db.drop_collection("Slot2")
db.drop_collection("Slot3")
db.drop_collection("address")
db.drop_collection("Data")

co = db.Slot1
f = open('slot1.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

co = db.Slot2
f = open('slot2.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

co = db.Slot3
f = open('slot3.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

co = db.address
f = open('address.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    data[line[0]] = line[1]
    co.insert(data)
f.close()

=======
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
>>>>>>> 1bc1b65ac1878cedd77f75b7551d0fdfe150c900
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


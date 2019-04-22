import pymongo
import csv
 

connection = pymongo.MongoClient("localhost", 27017)
db = connection.testDB

db.drop_collection("SlotData1")
db.drop_collection("SlotData2")
db.drop_collection("SlotData3")
db.drop_collection("Datas")


co = db.SlotData1
f = open('slotData1.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

co = db.SlotData2
f = open('slotData2.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

co = db.SlotData3
f = open('slotData3.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

for i in range(1, 4):
    collectionName = "SlotData" + str(i)
    co = db[collectionName]
    db.drop_collection(collectionName)
    f = open('slotData'+str(i)+'.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)
    for line in rdr:
        data = {}
        for num in range(len(line)):
            if num % 2 == 0:
                data[line[num]] = line[num + 1]
        co.insert(data)
    f.close()


db.drop_collection("Datas")

co = db.Datas
f = open('datas.csv', 'r', encoding='utf-8-sig')
rdr = csv.reader(f)
for line in rdr:
    data = {}
    for num in range(len(line)):
        if num % 2 == 0:
            data[line[num]] = line[num+1]
    co.insert(data)
f.close()

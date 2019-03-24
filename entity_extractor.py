import pymongo
import re

def get_entity(line, entity_list, num):
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.testDB
    collection_name = "Slot" + str(num)
    co = db[collection_name]
    for entity in co.distinct("EntityName"):
        if entity in line:
            entity_class = co.distinct("EntityClass", {"EntityName": entity})
            line = line.replace(entity, entity_class[0])
            entity_list.append(entity)
    return line, entity_list

def get_location(line, entity_list):
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.testDB
    collection_name = "address"
    co = db[collection_name]
    texts = line.split(' ')

    many_answers = []
    for entity in co.distinct("address"):
        for voca in texts:
            if voca in entity:
                many_answers.append(entity)

    if len(many_answers) > 1:
        return many_answers[0].split(' ')[2]
    else:
        return many_answers[0]


#print(get_location("광진구 금고 위치", []))
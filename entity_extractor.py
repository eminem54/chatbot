import pymongo


def get_entity1(line, entity_list):
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.testDB
    co = db.Slot1
    for entity in co.distinct("EntityName"):
        if entity in line:
            entity_class = co.distinct("EntityClass", {"EntityName": entity})
            line = line.replace(entity, entity_class[0])
            entity_list.append(entity)
    return line, entity_list


def get_entity2(line, entity_list):
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.testDB
    co = db.Slot2
    for entity in co.distinct("EntityName"):
        if entity in line:
            entity_class = co.distinct("EntityClass", {"EntityName": entity})
            line = line.replace(entity, entity_class[0])
            entity_list.append(entity)
    return line, entity_list


def get_entity3(line, entity_list):
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.testDB
    co = db.Slot3
    for entity in co.distinct("EntityName"):
        if entity in line:
            entity_class = co.distinct("EntityClass", {"EntityName": entity})
            line = line.replace(entity, entity_class[0])
            entity_list.append(entity)
    return line, entity_list

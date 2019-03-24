import pymongo


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
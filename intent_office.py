import pymongo
import re

class SlotOperator:
    def __init__(self, slot):
        self.slot = slot

    def find_address_by_db(self, msg):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for idx, it in enumerate(["Dong", "Ro", "Gu", "Si"]):
            co = db[it].find({})
            for address in co:
                for name in address.keys():
                    if name=='_id':
                        continue
                    else:
                        if msg.find(name) == 0:
                            self.slot.address.set_address_field(idx, name)
                            return name
        else:
            return None

    def slot_filling(self, address_list):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for idx, it in enumerate(["Dong", "Ro", "Gu", "Si"]):
            co = db[it]
            for address in address_list:
                result = co.find_one({address:'0'})
                if result:
                    self.slot.address.set_address_field(idx, result)
                    return address
        else:
            return None

    def find_address_keyword(self, msg):
        return re.findall('\D+[동,로,구]|\D\D+[동,로,구,]|\D\D\D+[동,로,구,시]|\D\D\D\D+[동,로,구]', msg)

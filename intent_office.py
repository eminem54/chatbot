import pymongo
import re

class SlotOperator:
    def __init__(self, slot, entity_list):
        self.slot = slot
        self.entity_list = entity_list

    def find_address_by_db(self, msg):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for it in ["Dong", "Ro", "Gu", "Si"]:
            co = db[it].find()
            for address in co.keys():
                if address=='_id':
                    continue
                else:
                    if msg.find(address) == 0:
                        return address
        else:
            return None


    def find_address(self, db, address):
        return db.find_one({address:'0'})

    def slot_filling(self, address_list):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for it in ["Dong", "Ro", "Gu", "Si"]:
            co = db[it]
            for address in address_list:
                result = self.fill_entity(co, address)
                if result:
                    return address
        else:
            return None

    def get_answer(self):
        answer = "새마을금고"
        if self.slot.entity[6] is not "":
            answer = answer + " " + self.slot.entity[6]
        if self.slot.entity[5] is not "":
            answer = self.slot.entity[5] + " " + answer
        if self.slot.entity[4] is not "":
            answer = self.slot.entity[4] + " " + answer

        return answer


    def find_address_keyword(self, msg):
        return re.findall('\D+[동,로,구]|\D\D+[동,로,구,]|\D\D\D+[동,로,구,시]|\D\D\D\D+[동,로,구]', msg)

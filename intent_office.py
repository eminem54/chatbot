import pymongo
import re

class SlotOperator:
    def __init__(self, slot, entity_list):
        self.slot = slot
        self.entity_list = entity_list

    def fill_entity(self, db, address):
        pass


    def slot_filling(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for it in ["Dong", "Ro", "Gu", "Si"]:
            collection_name_list = it
            co = db[it]
            result = self.fill_entity(co, it)
            if result:
                return True
        else:
            return False

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
        return re.findall('\D+[동,로,구,시]|\D\D+[동,로,구,시]|\D\D\D+[동,로,구,시]|\D\D\D\D+[동,로,구,시]|\D\D\D\D\D+[동,로,구,시]', msg)

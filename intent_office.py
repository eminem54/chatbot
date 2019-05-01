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
                    self.slot.address.set_address_field(idx, address)
                    return address
        else:
            return None

    def find_address_keyword(self, msg):
        return re.findall('\D+[동,로,구]|\D\D+[동,로,구]|\D\D\D+[동,로,구,시]|\D\D\D\D+[동,로,구]', msg)


    def not_found_address_entity(self, msg):
        find_address = self.find_address_by_db(msg)
        answer = ""
        if find_address: # 디비를 기준으로 메시지를 한번더 검사
            return find_address + " 새마을금고", True
        else: #없으면 사용자입력그대로
            return msg if msg != "지점 안내" else "지명을 입력해주세요.", False

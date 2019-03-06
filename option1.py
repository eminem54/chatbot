import pymongo


class Option1:
    def __init__(self, slot, entity1_list, entity2_list, entity3_list):
        self.slot = slot
        self.entity1List = entity1_list
        self.entity2List = entity2_list
        self.entity3List = entity3_list

    def fill_entity1(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Slot1
        if self.entity1List != []:
            for entity in self.entity1List:
                temp_class = co.distinct("EntityClass", {"EntityName": entity})[0]
            if temp_class == "상품분류":
                self.slot.entity1 = entity
            return 0
        return 1

    def fill_entity2(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Slot2
        if self.entity2List != []:
            for entity in self.entity2List:
                temp_class = co.distinct("EntityClass", {"EntityName": entity})[0]
            if temp_class == "상품명":
                self.slot.entity2 = entity
                return 0
        return 1

    def fill_entity3(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Slot3
        if self.entity3List != []:
            for entity in self.entity3List:
                temp_class = co.distinct("EntityClass", {"EntityName": entity})[0]
            if temp_class == "상세설명":
                self.slot.entity3 = entity
                return 0
        return 1

    def get_answer(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Data
        if self.slot.entity2 is not "" and self.slot.entity3 is not "":
            answer = co.distinct(self.slot.entity3, {"상품이름": self.slot.entity2})
            if answer == []:
                self.slot.clear()
                return "해당하는 정보가 없습니다"
            else:
                self.slot.clear()
                return answer[0]

        elif self.slot.entity2 is not "" and self.slot.entity3 is "":
            answer = co.distinct("상품설명", {"상품이름": self.slot.entity2})[0]
            self.slot.clear()
            return answer

        elif self.slot.entity1 is "" and self.slot.entity2 is "":
            self.slot.log = "1"
            answer = "상품의 종류를 입력해주세요"
            return answer

        elif self.slot.entity1 is not "" and self.slot.entity2 is "":
            self.slot.log = "2"
            answer = "상품의 이름을 입력해주세요"
            return answer

        elif self.slot.entity2 is not "" and self.slot.entity3 is "":
            answer = co.distinct("상품설명", {"상품이름": self.slot.entity2})[0]
            self.slot.clear()
            return answer

    def slot_filling(self):
        if self.slot.log is "":
            self.fill_entity3()
            self.fill_entity2()
            self.fill_entity1()
            return 0

        elif self.slot.log is "1":
            result = self.fill_entity1()
            if result is 1:
                self.slot.clear()
            return result

        elif self.slot.log is "2":
            result = self.fill_entity2()
            if result is 1:
                self.slot.clear()
            return result

        elif self.slot.log is "3":
            result = self.fill_entity3()
            if result is 1:
                self.slot.clear()
            return result

import pymongo


class SlotOperator:
    def __init__(self, slot, entity_list):
        self.slot = slot
        self.entity_list = entity_list

    def fill_entity(self, num):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        collection_name = "Slot" + str(num)
        co = db[collection_name]
        if self.entity_list[num] != []:
            for entity in self.entity_list[num]:
                temp_class = co.distinct("EntityClass", {"EntityName": entity})
                if temp_class != []:
                    if temp_class[0] == "상품분류" and num == 1:
                        self.slot.entity[num] = entity
                        return 0
                    elif temp_class[0] == "상품명" and num == 2:
                        self.slot.entity[num] = entity
                        return 0
                    elif temp_class[0] == "상세설명" and num == 3:
                        self.slot.entity[num] = entity
                        return 0
        return 1

    def get_answer(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Data
        if self.slot.entity[2] is not "" and self.slot.entity[3] is not "":
            answer = co.distinct(self.slot.entity[3], {"상품이름": self.slot.entity[2]})
            if answer == []:
                return "해당되는 정보가 없습니다", 1
            else:
                return answer[0], 1

        elif self.slot.entity[2] is not "" and self.slot.entity[3] is "":
            answer = co.distinct("상품설명", {"상품이름": self.slot.entity[2]})[0]
            return answer, 1

        elif self.slot.entity[1] is "" and self.slot.entity[2] is "":
            self.slot.log = "1"
            answer = "상품의 종류를 입력해주세요"
            return answer, 0

        elif self.slot.entity[1] is not "" and self.slot.entity[2] is "":
            self.slot.log = "2"
            answer = "상품의 이름을 입력해주세요"
            return answer, 0

        elif self.slot.entity[2] is not "" and self.slot.entity[3] is "":
            answer = co.distinct("상품설명", {"상품이름": self.slot.entity2})[0]
            return answer, 1

    def slot_filling(self):
        if self.slot.log is "":
            self.fill_entity(3)
            self.fill_entity(2)
            self.fill_entity(1)
            return 0

        elif self.slot.log is "1":
            return self.fill_entity(1)

        elif self.slot.log is "2":
            return self.fill_entity(2)

        elif self.slot.log is "3":
            return self.fill_entity(3)

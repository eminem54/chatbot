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
                    if temp_class[0] == "지점지역" and num == 4:
                        self.slot.entity[num] = entity
                        return 0
                    elif temp_class[0] == "지점시군구" and num == 5:
                        self.slot.entity[num] = entity
                        return 0
                    elif temp_class[0] == "지점영업점" and num == 6:
                        self.slot.entity[num] = entity
                        return 0
        return 1

    def slot_filling(self):
        if self.slot.log is "":
            for i in range(6, 3, -1):
                self.fill_entity(i)
            return 0
        else:
            return self.fill_entity(int(self.slot.log))

    def get_answer(self):
        answer = "새마을금고"
        if self.slot.entity[6] is not "":
            answer = answer + " " + self.slot.entity[6]
        if self.slot.entity[5] is not "":
            answer = self.slot.entity[5] + " " + answer
        if self.slot.entity[4] is not "":
            answer = self.slot.entity[4] + " " + answer

        return answer




import pymongo


class SlotOperator:
    def __init__(self, slot,recoentity_list):
        self.slot = slot
        self.recoentity_list = recoentity_list

    def fill_entity(self, num):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        collection_name = "Reco" + str(num)
        co = db[collection_name]
        if self.recoentity_list[num] != []:
            for recoentity in self.recoentity_list[num]:
                temp_class = co.distinct("RecoClass", {"RecoEntityNm": recoentity})
                if temp_class != []:
                    if temp_class[0] == "성별" and num == 1:
                        self.slot.recoentity[num] = recoentity
                        return 0
                    elif temp_class[0] == "나이" and num == 2:
                        self.slot.recoentity[num] = recoentity
                        return 0
                    elif temp_class[0] == "좋은" and num == 3:
                        self.slot.recoentity[num] = recoentity
                        return 0
                    elif temp_class[0] == "추천상품" and num == 4:
                        self.slot.recoentity[num] = recoentity
                        return 0

        return 1

    def receive_answer(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Recodata
        if self.slot.recoentity[3] is not "" and self.slot.recoentity[4] is not "":
            answer = co.distinct(self.slot.recoentity[4], {"직업이름": self.slot.recoentity[3]})
            if answer == []:
                return "해당되는 정보가 없습니다", 1
            else:
                return answer[0], 1

        elif self.slot.entity[3] is not "" and self.slot.entity[4] is "":  # 2: 상품명 3:상세설명은 없는경우
            answer = co.distinct("상품이름", {"상품종류": self.slot.entity[3]})[0]
            return answer, 1

        elif self.slot.recoentity[1] is "" and self.slot.recoentity[2] is "":
            self.slot.recolog = "1"
            answer = "성별을 입력해 주세요 (여자/남자)"
            return answer, 0

        elif self.slot.recoentity[1] is not "" and self.slot.recoentity[2] is "":
            self.slot.recolog = "2"
            answer = "20세 이상이신가요? (이상/이하)"
            return answer, 0

        elif self.slot.recoentity[2] is not "" and self.slot.recoentity[3] is "":
            self.slot.recolog = "3"
            answer = "무슨 일을 하시나요? (대학생/직장인/그외)"
            return answer, 0

            #elif self.slot.recoentity[3] is not "" and self.slot.recoentity[4] is "":
            #self.slot.recolog = "4"
            #answer = "제발살려줘"
            #return answer, 0

        elif self.slot.entity[3] is not "" and self.slot.entity[4] is "":
            answer = co.distinct("상품이름", {"상품종류": self.slot.recoentity3})[0]
            return answer, 1

    def slot_filling(self):
        if self.slot.recolog is "":
            self.fill_entity(4)
            self.fill_entity(3)
            self.fill_entity(2)
            self.fill_entity(1)
            return 0

        elif self.slot.recolog is "1":
            return self.fill_entity(1)

        elif self.slot.recolog is "2":
            return self.fill_entity(2)

        elif self.slot.recolog is "3":
            return self.fill_entity(3)

        elif self.slot.recolog is "4":
            return self.fill_entity(4)



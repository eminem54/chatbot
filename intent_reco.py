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
                    if temp_class[0] == "추천성별클래스" and num == 1:
                        self.slot.recoentity[num] = recoentity
                        return 0
                    elif temp_class[0] == "추천종류클래스" and num == 2:
                        self.slot.recoentity[num] = recoentity
                        return 0
                    elif temp_class[0] == "추천직업클래스" and num == 3:
                        self.slot.recoentity[num] = recoentity
                        return 0
                    elif temp_class[0] == "추천상품클래스" and num == 4:
                        self.slot.recoentity[num] = recoentity
                        return 0

        return 1

    def receive_answer(self):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Recodata
        conv = db.ProductRecommend
        if self.slot.recoentity[3] is not "" and self.slot.recoentity[4] is not "":
           #congender = conv.distinct(self.slot.recoentity[1],{"성별":self.slot.recoentity[1]})
           answer = co.distinct(self.slot.recoentity[4], {"직업": self.slot.recoentity[3],"성별":self.slot.recoentity[1],
                                                           "상품종류": self.slot.recoentity[2]})
           if answer == []:
                self.get_data_button(3)
                return "해당되는 정보가 없습니다", 0
           else:
                return answer[0], 1

        elif self.slot.recoentity[3] is not "" and self.slot.recoentity[4] is "":
           # congender = conv.distinct("변환", {"성별": self.slot.recoentity1})
            gender = self.slot.recoentity[1]
            answer = co.distinct("상품설명", {"직업": self.slot.recoentity[3],"성별": gender,"상품종류": self.slot.recoentity[2]})[0]
            return answer, 1

        elif self.slot.recoentity[1] is "" and self.slot.recoentity[2] is "":
            self.slot.recolog = "1"
            answer = "성별을 입력해 주세요 (여자/남자)"
            self.get_data_button(1)
            return answer, 0

        elif self.slot.recoentity[1] is not "" and self.slot.recoentity[2] is "":
            self.slot.recolog = "2"
            answer = "예금/대출"
            self.get_data_button(2)
            return answer, 0

        elif self.slot.recoentity[2] is not "" and self.slot.recoentity[3] is "" and self.slot.recoentity[1]is not "":
            self.slot.recolog = "3"
            answer = "무슨 일을 하시나요? (대학생/직장인/그외)"
            self.get_data_button(3)
            return answer, 0

        elif self.slot.recoentity[3] is not "" and self.slot.recoentity[4] is "":
            gender = self.slot.recoentity1
            answer = co.distinct("상품설명", {"직업": self.slot.recoentity3,"성별": gender,"상품종류": self.slot.recoentity2})[0]
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

    def get_data_button(self,num):
        if num == 1:
            self.slot.button = ['남자', '여자']
            self.slot.button_list = [['남자', '남자추천성별이름봇'], ['여자', '여자추천성별이름봇']]
            return
        if num == 2:
            self.slot.button = ['예금', '대출']
            self.slot.button_list = [['예금', '예추천이름봇'], ['대출', '대추천이름봇']]
            return
        if num == 3:
            self.slot.button = ['대학생', '직장인', '그외',]
            self.slot.button_list = [['대학생', '직장인', '그외',], ['대직업이름봇', '직직업이름봇','그외직업이름봇']]
            self.slot.button_list = [['대학생', '대직업이름봇'], ['직장인', '직직업이름봇'], ['그외', '그외직업이름봇']]
            return
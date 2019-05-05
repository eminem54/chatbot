import pymongo


class SlotOperator:
    def __init__(self, slot, entity_list):
        self.slot = slot
        self.entity_list = entity_list

    def fill_entity(self, num):     # entity 채우기 성공 시 1, 실패 시 0 반환
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

    def get_answer(self):       # 답변 출력, 0: 완벽 답변, 슬롯 클리어 / 1: 불완전 답변, 슬롯 보존
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Data
        if self.slot.entity[2] is not "" and self.slot.entity[3] is not "":
            answer = co.distinct(self.slot.entity[3], {"상품이름": self.slot.entity[2]})
            if answer == []:
                self.get_button_list(3)
                return "상품이 가진 항목의 입력이 잘못되었습니다.", 0
            else:
                return answer[0], 1

        elif self.slot.entity[2] is not "" and self.slot.entity[3] is "":       # 2: 상품명 3:상세설명은 없는경우
            answer = ""
            post = co.find_one({"상품이름": self.slot.entity[2]})
            for postItem in post.items():
                if postItem[0] != "_id" and postItem[0] != "상품종류" and postItem[0] != "":
                    answer += postItem[1] + "\n\n"
            return answer, 1

        elif self.slot.entity[1] is "" and self.slot.entity[2] is "":
            self.slot.log = "1"
            answer = "상품의 종류를 입력해주세요."
            self.get_button_list(1)
            return answer, 0

        elif self.slot.entity[1] is not "" and self.slot.entity[2] is "":
            self.slot.log = "2"
            answer = "상품의 이름을 입력해주세요."
            self.get_button_list(2)
            return answer, 0

    def slot_filling(self):
        if self.slot.log is "":     # 슬롯 로그가 비워져있다면 모든 슬롯 채우고 0 반환
            self.fill_entity(3)
            self.fill_entity(2)
            self.fill_entity(1)
            return 0    # 0 : 슬롯이 정상적으로 채워짐, 1 : 슬롯 로그에 맞게 채워지지 않음

        elif self.slot.log is "1":
            return self.fill_entity(1)  # "fill_entity"의 반환값은 채우기 성공 시 0, 실패 시 1 이며, 함수 인자를 통해 로그에 맞는 슬롯이 채워지도록 시도

        elif self.slot.log is "2":
            return self.fill_entity(2)

        elif self.slot.log is "3":

            return self.fill_entity(3)


    def get_button_list(self, num):
        button_list = set()
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        co = db.Data

        if num == 1:
            post = co.distinct("상품종류")
            for postItem in post:
                button_list.add(postItem)
            self.slot.button = list(button_list)
            print(self.slot.button)
            return

        if num == 2:
            post = co.distinct("상품이름", {"상품종류": self.slot.entity[1]})
            for postItem in post:
                button_list.add(postItem)
            self.slot.button = list(button_list)
            print(self.slot.button)
            return

        if num == 3:
            post = co.find_one({"상품이름": self.slot.entity[2]})
            for postItem in post.items():
                if postItem[0] != "_id" and postItem[0] != "상품종류" and postItem[0] != "상품이름" and postItem[0] != "":
                    button_list.add(postItem[0])
            self.slot.button = list(button_list)
            print(self.slot.button)
            return
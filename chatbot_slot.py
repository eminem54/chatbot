class Slot:
    #상품분류
    entity1 = ""
    #상품명
    entity2 = ""
    #상세설명\
    entity3 = ""
    #지점지역
    entity4 = ""
    #지점시군구
    entity5 = ""
    #지점영업점
    entity6 = ""

    entity = ["" for _ in range(7)]

    intent = ""
    log = ""

    def clear(self):
        self.entity1 = ""
        self.entity2 = ""
        self.entity3 = ""
        self.entity4 = ""
        self.entity5 = ""
        self.entity6 = ""

        for i in range(7):
            self.entity[i] = ""

        self.intent = ""
        self.log = ""
        return 0


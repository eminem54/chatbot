class Address:
    def __init__(self):
        self.Si = None
        self.Gu = None
        self.Ro = None
        self.Dong = None

    def empty(self):
        if self.Si is None and self.Gu is None and self.Ro is None and self.Dong is None:
            return True
        else:
            return False

    def set_address_field(self, index, value):
        if index is 0:
            self.Dong = value
        elif index is 1:
            self.Ro = value
        elif index is 2:
            self.Gu = value
        elif index is 3:
            self.Si = value

class Slot:
    #상품분류0
    entity1 = ""
    #상품명1
    entity2 = ""
    #상세설명\2
    entity3 = ""
    #주소저장클래스3
    address = Address()
    #성별
    recoentity1 = ""
    #나이
    recoentity2 = ""
    #직업
    recoentity3 = ""

    recoentity4 = ""
    button = []

    entity = ["" for _ in range(4)]
    recoentity = ["" for _ in range(5)]
    intent = ""
    log = ""
    recointent = ""
    recolog = ""

    def clear(self):
        self.entity1 = ""
        self.entity2 = ""
        self.entity3 = ""

        for i in range(4):
            self.entity[i] = ""

        self.intent = ""
        self.log = ""
        return 0

    def recoClear(self):
        self.recoentity1 = ""
        self.recoentity2 = ""
        self.recoentity3 = ""
        self.recoentity4 = ""

        for j in range(5):
            self.recoentity[j] = ""

        self.recointent = ""
        self.recolog = ""
        return 0

    def print_slot(self):
        print(f'상품분류: {self.entity[1]} 상품명: {self.entity[2]} 상세설명: {self.entity[3]} 시: {self.address.Si} '
              f'구: {self.address.Gu} 로: {self.address.Ro} 동: {self.address.Dong} 성별: {self.recoentity[1] } 나이: {self.recoentity[2]}'
              f'recolog: {self.recolog} 추천의도: {self.recointent} 설명: {self.recoentity[4]} log: {self.log} 의도: {self.intent} 직업: {self.recoentity[3]}')

    def clone_slot(self, source):
        pass
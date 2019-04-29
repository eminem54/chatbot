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

    button = []

    entity = ["" for _ in range(4)]
    intent = ""
    log = ""

    def clear(self):
        self.entity1 = ""
        self.entity2 = ""
        self.entity3 = ""

        for i in range(4):
            self.entity[i] = ""

        self.intent = ""
        self.log = ""
        return 0


    def print_slot(self):
        print('상품분류: {self.entity[1]} 상품명: {self.entity[2]} 상세설명: {self.entity[3]} 시: {self.address.Si} '
              '구: {self.address.Gu} 로: {self.address.Ro} 동: {self.address.Dong} log: {self.log} 의도: {self.intent}')

    def clone_slot(self, source):
        pass
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


class Slot:
    #상품분류0
    entity1 = ""
    #상품명1
    entity2 = ""
    #상세설명\2
    entity3 = ""
    #주소저장클래스3
    address = Address()

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



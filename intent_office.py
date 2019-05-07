import pymongo
import re


def location_service_routine(msg, slot):
    module = SlotOperator(slot)  # 엔티티추출기클래스
    address_list = module.find_address_keyword(msg)  # 시구로동역을 뽑아서 배열로
    find_address = module.slot_filling(address_list)  # 슬롯을 채운다

    if find_address:  # 슬롯필링후 찾으면
        answer = find_address
        slot.address.answer_find = True
    else:  # 못찾으면
        answer = module.not_found_address_entity(msg)

        if answer is not None:  # 디비기준으로검사해서 찾으면
            slot.address.answer_find = True
        else:  # 못찾으면
            if len(address_list) > 0:  # 지정한 키워드 하나라도 찾으면 찾은것
                answer = address_list[0]
                slot.address.answer_find = True
            else:  # 끝내못찾았다
                slot.button = ['도봉구', '마포구', '관악구', '강북구', '용산구', '서초구', '노원구', '성동구', '강남구',
                               '성북구', '광진구', '송파구', '은평구', '강서구', '강동구', '종로구', '양천구', '중랑구',
                               '영등포구', '서대문구', '구로구', '동대문구', '동작구', '중구', '금천구']

    return answer


class SlotOperator:
    def __init__(self, slot):
        self.slot = slot

    def find_address_by_db(self, msg):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for idx, it in enumerate(["Dong", "Ro", "Gu", "Si"]):
            co = db[it].find({})
            for address in co:
                for name in address.keys():
                    if name == '_id':
                        continue
                    else:
                        if msg.find(name) == 0:
                            self.slot.address.set_address_field(idx, name)
                            return name
        else:
            return None

    def slot_filling(self, address_list):
        connection = pymongo.MongoClient("localhost", 27017)
        db = connection.testDB
        for idx, it in enumerate(["Dong", "Ro", "Gu", "Si"]):
            co = db[it]
            for address in address_list:
                result = co.find_one({address:'0'})
                if result:
                    self.slot.address.set_address_field(idx, address)
                    return address
        else:
            return None

    def find_address_keyword(self, msg):
        return re.findall('[^ \t\n\r\f0-9]{1,7}[동,로,구,역,병원,대,공원]', msg)

    def not_found_address_entity(self, msg):
        find_address = self.find_address_by_db(msg)
        answer = ""
        if find_address: # 디비를 기준으로 메시지를 한번더 검사 성공시
            return find_address
        else:  # 없으면 return None
            return None



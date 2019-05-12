import pymongo
from konlpy.tag import Mecab

mecab = Mecab(dicpath="C:\\mecab\\mecab-ko-dic")


class ConversionClass:
    msg_pos_result = []
    msg_pos_len = 0
    file_name = "ConversionData"
    connection = pymongo.MongoClient("localhost", 27017)
    db = connection.testDB
    db.drop_collection(file_name)
    co = db[file_name]

    def tag_input_msg(self, input_msg):
        msg_pos_list = mecab.pos(input_msg)  # 입력 메시지를 형태소 분석
        for msg_pos in msg_pos_list:
            if msg_pos[1][0] == "N" or msg_pos[1][0] == "V":    # 형태소가 명사, 동사일 경우
                ConversionClass.msg_pos_result.append(msg_pos[0])
        ConversionClass.msg_pos_result.sort()
        ConversionClass.msg_pos_len = len(ConversionClass.msg_pos_result)

    def clear_conversion_data(self):
        ConversionClass.msg_pos_result = []
        ConversionClass.msg_pos_len = 0

    def add_conversion_data(self, input_msg, conversion_msg):
        self.tag_input_msg(input_msg)
        self.co.update({"입력문장": ConversionClass.msg_pos_result}, {"$set": {"변환문장": conversion_msg}}, upsert=True)
        self.clear_conversion_data()

    def is_existed_conversion_data(self):    # 입력 문장을 DB에 몇 개 존재하는지 세고 0개가 아니라면 True 반환
        num = self.co.count_documents({"입력문장": ConversionClass.msg_pos_result})
        print("입력문장:", ConversionClass.msg_pos_result)
        print("num:", num)
        if num == 0:
            return False
        else:
            return True

    def get_conversion_data(self, input_msg):   # DB에 데이터가 있다면 문장을 변환
        self.tag_input_msg(input_msg)
        return self.co.distinct("변환문장", {"입력문장": ConversionClass.msg_pos_result})


# conversion = "상품소개 대출 알려줘"
# test_input = "예금 금리 알려줘"
#
# cc = ConversionClass()
# cc.add_conversion_data(test_input, conversion)
# print(cc.get_conversion_data(test_input))

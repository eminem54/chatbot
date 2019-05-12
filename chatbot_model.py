import entity_extractor
import chatbot_slot
import intent_product
import intent_office
import intent_reco
import keras_intent_extract
import copy
import refine_sentence
import data_tfidf
import generative_model_predict as gm

slot = chatbot_slot.Slot()
dc_obj = data_tfidf.dc.ConversionClass()


class ChatBot:
    def intent_extraction(self, msg):
        msg = refine_sentence.refine_sentence(msg)
        return keras_intent_extract.evaluation(msg)

    def convert_msg(self, msg):
        if dc_obj.is_existed_conversion_data(msg):
            print("컨버팅 있음")
            return dc_obj.get_conversion_data(msg)
        else:
            print("컨버팅 없음")
            return msg

    def run(self, msg):
        msg = self.convert_msg(msg)
        msg = refine_sentence.refine_sentence(msg)
        slot_result = 0

        entity_list = [[0 for cols in range(5)] for rows in range(4)] # 엔티티추출을위한 리스트
        recoentity_list = [[0 for cols in range(7)] for rows in range(6)]
        line = msg
        for i in range(3, 0, -1):  # 라인은 엔티티가 대체된 메세지
            line, entity_list[i] = entity_extractor.get_entity(line, entity_list[i], i)
        for i in range(5, 0, -1):
            line, recoentity_list[i] = entity_extractor.get_Recoentity(line, recoentity_list[i], i)
        line = entity_extractor.get_location(line)  # 지점안내를 위한 엔티티추출과 단어대체

        intent = ""
        if data_tfidf.is_unknown(line, data_tfidf.TFIDF_MATRIX):
            intent = "UnKnown"
        else:
            intent = self.intent_extraction(line)  # 엔티티로 대체된 문장으로 의도추출
        print(intent)

        answer = ""
        if slot.intent == "":
            slot.intent = intent

        if slot.intent == "상품 소개":
            module = intent_product.SlotOperator(slot, entity_list)
            result = module.slot_filling()
            if result is 0:
                answer, slot_result = module.get_answer()
            elif result is 1:
                slot.clear()
                return self.run(msg)

        elif slot.intent == "지점 안내":
            answer = intent_office.location_service_routine(msg, slot)

        elif slot.intent == "상품 추천":
            module = intent_reco.SlotOperator(slot, recoentity_list)
            result = module.slot_filling()
            if result is 0:
                answer, slot_result = module.receive_answer()
            elif result is 1:
                slot.recoClear()
                return self.run(msg)

        elif slot.intent == "UnKnown":
            answer = gm.make_generative_answer(msg)

        store_slot = copy.deepcopy(slot)
        slot.button = []
        if slot_result == 1 or slot.intent == "지점 안내" or slot.intent == "UnKnown" or slot.intent == "상품 추천":
            slot.clear()
        return answer, store_slot

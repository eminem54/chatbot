import entity_extractor
import chatbot_slot
import intent_product
import intent_office
import keras_intent_extract
import copy
import refine_sentence

slot = chatbot_slot.Slot()


class ChatBot:

    def intent_extraction(self, msg):
        msg = refine_sentence.refine_sentence(msg)
        return keras_intent_extract.evaluation(msg)

    def run(self, msg):
        msg = refine_sentence.refine_sentence(msg)
        slot_result = 0

        entity_list = [[0 for cols in range(5)] for rows in range(4)] #엔티티추출을위한 리스트
        line = msg
        for i in range(3, 0, -1): #w 라인은 엔티티가 대체된 메세지
            line, entity_list[i] = entity_extractor.get_entity(line, entity_list[i], i)
        line = entity_extractor.get_location(line) #지점안내를 위한 엔티티추출과 단어대체
        intent = self.intent_extraction(line)
        print(intent)
        #엔티티로 대체된 문장으로 의도추출

        answer = ""
        #if slot.intent is "":
        slot.intent = intent

        if slot.intent == "상품 소개":
            module = intent_product.SlotOperator(slot, entity_list)
            result = module.slot_filling()
            if result is 0:
                answer, slot_result = module.get_answer()
            elif result is 1:
                slot.clear()
                return self.run(msg)

        elif slot.intent == "지점 안내": #입력라인으로 뽑아낸 데이터가 지점안내인경우에
            answer = intent_office.location_service_routine(msg, slot)

        elif slot.intent == "고객 상담":
            slot.clear()
            answer = "고객 상담입니다"

        # print("의도: ", slot.intent, "log: ", slot.log, "대답: ", answer, "type(answer): ", type(answer))
        # for i in range(1, 4):
        #     print("entity" + str(i) + ": ", slot.entity[i], end='')

        slot.print_slot()
        store_slot = copy.deepcopy(slot)
        if slot_result == 1 or slot.intent == "지점 안내": #비어있을때가아니라 지점안내를 거치고나면 지우도록바꾸자
            slot.clear()
        return answer, store_slot


#bot = ChatBot()
#bot.run("서울 마포구 새마을금고 지역 안내해줘")
#bot.run("스피드마이너스대출")

import entity_extractor
import chatbot_slot
import intent_product
import intent_office
import keras_intent_extract
import copy

slot = chatbot_slot.Slot()


class ChatBot:

    def intent_extraction(self, msg):
        return keras_intent_extract.evaluation(msg)

    def run(self, msg):
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
            module = intent_office.SlotOperator(slot) #엔티티추출기클래스
            address_list = module.find_address_keyword(msg) #시구로동을 뽑아서 배열로
            find_address = module.slot_filling(address_list) #슬롯을 채운다

            if find_address: #슬롯필링후 찾으면
                answer = find_address + " 새마을금고"
                slot.address.answer_find = True
            else: #못찾으면
                answer, is_find = module.not_found_address_entity(msg)

                if is_find:
                    slot.address.answer_find = True
                else:
                    slot.address.answer_find = False
                    if len(address_list) > 0:
                        answer = address_list[0] + "새마을금고"
                        slot.address.answer_find = True

        elif slot.intent == "고객 상담":
            slot.clear()
            answer = "고객 상담입니다"

        # print("의도: ", slot.intent, "log: ", slot.log, "대답: ", answer, "type(answer): ", type(answer))
        # for i in range(1, 4):
        #     print("entity" + str(i) + ": ", slot.entity[i], end='')

        slot.print_slot()
        store_slot = copy.deepcopy(slot)
        if slot_result == 1 or not slot.address.empty():
            slot.clear()
        return answer, store_slot


#bot = ChatBot()
#bot.run("서울 마포구 새마을금고 지역 안내해줘")
#bot.run("스피드마이너스대출")

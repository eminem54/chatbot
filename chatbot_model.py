import entity_extractor as en
import chatbot_slot as cs
import intent_product
import intent_office
import keras_intent_extract

slot = cs.Slot()


class ChatBot:
    def intent_extraction(self, msg):
        return keras_intent_extract.evaluation(msg)

    def run(self, msg):
        line = msg
        slot_result = 0
        entity_list = [[0 for cols in range(5)] for rows in range(7)]
        answer = ""
        for i in range(6, 0, -1):
            line, entity_list[i] = en.get_entity(line, entity_list[i], i)
        intent = self.intent_extraction(line)

        if slot.intent is "":
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
            module = intent_office.SlotOperator(slot, entity_list)
            result = module.slot_filling()
            if result is 0:
                answer = module.get_answer()
            elif result is 1:
                slot.clear()
                return self.run(msg)

        elif slot.intent == "고객 상담":
            slot.clear()
            answer = "고객 상담입니다"

        print("의도: ", slot.intent)
        for i in range(1, 7):
            print("entity" + str(i) + ": ", slot.entity[i])
        print("log: ", slot.log)
        print("대답: ", answer)
        print("type(answer): ", type(answer))

        store_slot = slot

        if slot_result == 1:
            slot.clear()

        return answer, store_slot


#bot = ChatBot()
#bot.run("서울 마포구 새마을금고 지역 안내해줘")
#bot.run("스피드마이너스대출")

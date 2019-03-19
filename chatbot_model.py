import entity_extractor as en
import chatbot_slot as cs
import intent_product
import keras_intent_extract

slot = cs.Slot()


class ChatBot:
    def intent_extraction(self, msg):
        return keras_intent_extract.evaluation(msg)

    def run(self, msg):
        line = msg
        entity_list = [[0 for cols in range(5)] for rows in range(7)]

        line, entity_list[3] = en.get_entity(line, entity_list[3], 3)
        line, entity_list[2] = en.get_entity(line, entity_list[2], 2)
        line, entity_list[1] = en.get_entity(line, entity_list[1], 1)
        intent = self.intent_extraction(line)

#        for i in range(6, 0, -1):
#            line, entity_list[i] = en.get_entity(line, entity_list[i], i)

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

        elif slot.intent == "지점 안내":
            slot.clear()
            answer = "지점 안내입니다"

        elif slot.intent == "고객 상담":
            slot.clear()
            answer = "고객 상담입니다"

        print("의도: ", slot.intent)
        print("entity1: ", slot.entity1)
        print("entity2: ", slot.entity2)
        print("entity3: ", slot.entity3)
        print("log: ", slot.log)
        print("대답: ", answer)
        print("type(answer): ", type(answer))

        if slot_result == 1:
            slot.clear()

        return answer, slot.intent, slot.entity1, slot.entity2, slot.entity3


#bot = ChatBot()
#bot.run("대출 상품의 대출기간을 알려줘")
#bot.run("스피드마이너스대출")

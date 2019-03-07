import entity_extractor as en
import chatbot_slot as cs
import option1 as opt1
import keras_intent_extract

slot = cs.Slot()


class ChatBot:
    def intent_extraction(self, msg):
        return keras_intent_extract.evaluation(msg)

    def run(self, msg):
        line = msg
        entity1_list = []
        entity2_list = []
        entity3_list = []

        line, entity3_list = en.get_entity3(line, entity3_list)
        line, entity2_list = en.get_entity2(line, entity2_list)
        line, entity1_list = en.get_entity1(line, entity1_list)
        intent = self.intent_extraction(line)

        if slot.intent is "":
            slot.intent = intent

        if slot.intent == "상품 소개":
            module = opt1.Option1(slot, entity1_list, entity2_list, entity3_list)
            result = module.slot_filling()
            if result is 0:
                answer, slot_result = module.get_answer()
            if result is 1:
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


# bot = ChatBot()
# bot.run("대출 상품의 대출기간을 알려줘")
# bot.run("스피드마이너스대출")

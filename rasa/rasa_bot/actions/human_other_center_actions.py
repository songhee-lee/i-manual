import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker

logger = logging.getLogger(__name__)
#추후 밑에 클래스 복사해서 사용
class ActionLeadingOtherCenters1(Action):
    def name(self) -> Text:
        return "action_leading_other_centers1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_other_centers1')
        #기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        priority = []
        definedCnt = 0

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn":"김재헌", "ct":[1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t":3, "p":52}
        print("MetaData: ", metadata)
        dispatcher.utter_message(
            "그럼 마지막으로 남은 3개의 센터에 대해 살펴보겠습니다.")

        print("get Step")
        print(tracker.get_slot('step'))
        print("get Step end")

        if metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            msg = "항상 몸에 활력 에너지가 있는 당신은 다른 사람들의 지속적인 에너지 사용에 영향을 주는 사람입니다. 자신이 좋아하거나 사랑하는 일을 위해서라면 몇날 며칠을 밤을 새우더라도 그 일이 신이난다면 괜찮을 수 있는 당신은 엄청난 에너지를 지니고 있습니다. "
            msg2 = "이 에너지는 당신이 ‘결정 방식’에 따라 맞게 결정을 했을 때, 몸에서 만들어집니다. 하지만 당신은 대부분 에너지가 없는 상태로 지낼 것입니다. 왜냐하면? 자신의 결정 방식을 따르지 않았기 때문입니다. 그에 따른 결과는 만성피로에 시달리는, 활력없는 당신입니다."
            msg3 = "반면에 자신의 결정 방식을 따라 맞게 결정한 무언가에 대해서는 당신의 몸이 에너지를 만들어낼 것이기 때문에 지치지 않고 계속 할 수 있습니다. "
            msg4 = "몸이 에너지를 낼 수 있는지를 알기위해 주변 사람들에게 “Yes” or ”No”로 답이 가능한 형태의 질문을 받아야 합니다. 그리고 자신의 결정 방식에 따라 맞는 결정을 한다면 당신은 늘 활기찰 수 있습니다. 전체 인류의 약 66%가 이 에너지를 고정적으로 가지고 있습니다."
        else:
            h_type = "활력 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 오는 활력 에너지에 열려있는 당신은 에너지 효율에 대한 아이디어가 있는 사람입니다. 더 일하고, 더 공부하고, 더 놀고, 더 자고, 더 먹고 등등. 당신은 늘 아쉽습니다. 더 해야할 것 같고, 더 했으면 좋겠는데 생각과 달리 체력이 따라주지 않습니다. "
            msg2 = "그럼에도 늘 ‘더 하고 싶어!! 더 할거야!!!’ 라고 생각하며 늘 지나치게 무언가를 합니다. 자신에게는 활력 에너지가 없는데도 마치 가지고 있는 것처럼 착각하는 것입니다. 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. 이로 인해 당신은 모든 것에 있어서 충분한 때를 모릅니다. "
            msg3 = "그래서 지나치게 무언가를 하고 몸에 무리가 와 힘들어하기 쉽습니다. 밖에서는 힘차게 있다가 집으로 돌아오면 극심한 피로를 느끼며 지쳐 쓰러지듯 잠드는 것이 자신의 모습이라면, 주의해야합니다. 계속해서 무리하게 에너지를 쥐어짜며 살다가는 자기 자신의 건강을 해치기 쉽기 때문입니다. "
            msg4 = "당신은 활력 에너지를 통해 생산적인 일을 하는 사람이 아닙니다. 절대 무리하지 말고, 되도록 많이 많이 쉬어야 합니다. 전체 인류의 약 34%는 이 센터가 정의되어 있지 않습니다."
        dispatcher.utter_message(f'{metadata["pn"]}님의 "{h_type}"에 대해서 설명드릴께요!', image=img)
        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)
        dispatcher.utter_message(msg3)
        dispatcher.utter_message(msg4)
        buttons = []
        buttons.append({"title": f'동의합니다', "payload": "/leading_other_centers2"})
        buttons.append({"title": f'동의하지 않습니다', "payload": "/leading_other_centers2"})
        #response = tracker.get_slot('result') 원하는 부분에 붙여넣기
        dispatcher.utter_message(f'이 설명에 대해서 동의하시나요?(마스터봇질문)', buttons=buttons)

        return []
class ActionLeadingOtherCenters2(Action):
    def name(self) -> Text:
        return "action_leading_other_centers2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_other_centers2')
        #기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        priority = []
        definedCnt = 0

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn":"김재헌", "ct":[1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t":3, "p":52}
        print("MetaData: ", metadata)

        print("get Step")
        print(tracker.get_slot('step'))
        print("get Step end")

        if metadata["ct"][7] == 1: #이부분 수정
            h_type = "생각 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7.gif"
            msg = "항상 자기만의 방식으로 생각하고 개념화하는 당신은 다른 사람들의 사고방식에 영향을 주는 사람입니다. 생각하고 의견을 내는데에 있어서 당신은 일정한 방식이 있습니다. "
            msg2 = "도표나 그림을 떠올리며 생각을 하기도 하고, 어떤 소리가 들려와 생각하기도 하고, 과거에 했던 경험을 바탕으로 생각을 하는 등의 과정을 거쳐 자기만의 의견을 가지게 됩니다. "
            msg3 = "이렇게 형성된 당신의 의견은 좀처럼 바뀌지 않고, 외부의 영향에도 잘 흔들리지 않습니다. 자기 신념이 확고한 것이라고 할 수 있습니다. "
            msg4 = "또한 당신은 무언가를 이해하려 집착적으로 생각하다가 근심에 휩싸일 수 있지만 생각은 생각일 뿐, 행동은 하시면 안됩니다. 전체 인류의 약 47%가 이 에너지를 고정적으로 가지고 있습니다."
        else:
            h_type = "생각 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 오는 다양한 사고방식에 열려있는 당신은 정보를 스폰지 처럼 흡수하는 사람입니다. 다양한 사고방식에 열려있는 당신은 사람, 책, 미디어 등 모든 것에서 오는 다양한 정보들이 흥미롭습니다. ‘이런 의견도 있구나. 저렇게 생각할 수도 있겠는데? 이 정보도 일리가 있어.’ 라고 생각합니다. "
            msg2 = "하지만 다른 한 편으로는 ‘나는 왜 다 일리가 있다고 할까? 왜 자꾸 생각이나 의견이 바뀌지? 귀가 얇은가?’ 라는 생각도 듭니다. 흔히 말하는 팔랑귀, 그것이 바로 당신의 건강한 모습입니다. 팔랑귀라고 해서 무조건 나쁜 것이 아닙니다."
            msg3 = "이것을 문제로 여기기 시작할 때, 다양한 생각과 의견에 대한 당신의 열린 자세는 닫힌 자세로 바뀌어 특정 생각이나 의견에 자신을 묶어버립니다. 그리고 자신의 생각과 의견만이 맞다고 합니다. 아주 고집스러워지는 것입니다. 영원히 바뀌지 않을 생각과 의견이 세상에 존재하기는 할까요? "
            msg4 = "당신에게는 어떤 생각이 더 좋은 것이고, 어떤 의견이 더 맞는 것인지 잘 구별할 수 있는 잠재성이 있습니다.전체 인류의 약 53%는 이 센터가 정의되어 있지 않습니다."
        dispatcher.utter_message(f'다음은 {metadata["pn"]}님의 "{h_type}"에 대해서 설명드릴께요!', image=img)
        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)
        dispatcher.utter_message(msg3)
        dispatcher.utter_message(msg4)
        buttons = []
        buttons.append({"title": f'동의합니다', "payload": "/leading_other_centers3"})
        buttons.append({"title": f'동의하지 않습니다', "payload": "/leading_other_centers3"})
        #response = tracker.get_slot('result') 원하는 부분에 붙여넣기
        dispatcher.utter_message(f'이 설명에 대해서 동의하시나요?(마스터봇질문)', buttons=buttons)

        return []

class ActionLeadingOtherCenters3(Action):
    def name(self) -> Text:
        return "action_leading_other_centers3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_other_centers3')
        #기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        priority = []
        definedCnt = 0

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn":"김재헌", "ct":[1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t":3, "p":52}
        print("MetaData: ", metadata)

        print("get Step")
        print(tracker.get_slot('step'))
        print("get Step end")

        if metadata["ct"][8] == 1: #이부분 수정
            h_type = "영감 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8.gif"
            msg = "항상 머릿속에 떠오르는 의문에 대한 답을 찾는 당신은 다른 사람들이 무언가에 대해 생각하도록 영감을 주는 사람입니다. "
            msg2 = "때때로 과거의 경험이 떠올라 혼란스러울 수 있고(‘도대체 그 일이 왜 자꾸 떠오르지?’), 무언가에 대한 의심이 들고(‘어? 이거 뭔가 이상한데? 뭔가 안맞는데?’), 알듯 말듯한 것을 명확히 알고싶겠지만(‘이게 뭘까? 뭐지? 알 것도 같은데..’) "
            msg3 = "이것은 단지 당신이 세상을 이해하기 위한 현상이라는 사실을 알아야 합니다. 억지로 답을 찾으려는 노력을 하는 동안에는 답이 보이지 않고, 답을 찾기를 멈추었을 때, 답을 보게 될 것입니다. "
            msg4 = "전체 인류의 약 30%가 이 에너지를 고정적으로 가지고 있습니다."
        else:
            h_type = "영감 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8_off.png"
            msg = "다른 사람이나 다른 무언가로부터 영감을 받는 당신은 ‘누가 나에게 혼란을 주고, 누가 나에게 영감을 주는지’를 잘 알 수 있는 사람입니다."
            msg2 = "평소에 생각이 많지 않다가 어떤 때에는 지나치게 생각이 많아져서 머리가 지끈거리거나, 생각을 하고 또 하고 또 하다가 불면증에 시달린 경험들 있습니까? 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. "
            msg3 = "이로 인해 당신은 위와 같은 현상을 겪을 수 있지만 이는 당신의 문제가 아닙니다. 또한 각종 영화, 드라마, 콘서트, 책, 강의, 전시회 등 영감을 주는 재미있는 것들을추구하게 되기 때문에 ‘오, 이거 재미있을 것 같아. 이건 나에게 영감을 줄것 같아. 이건 해야해!! ’라는 생각을 하며 온갖 것들을 합니다."
            msg4 = "온갖 영감을 받기위해 했던 많은 것들이 모두 당신에게 영감을 주었나요? 당신에게는 혼란과 영감을 잘 구별할 수 있는 잠재성이 있습니다. 전체 인류의 약 70%는 이 센터가 정의되어 있지 않습니다."
        dispatcher.utter_message(f'다음은 {metadata["pn"]}님의 "{h_type}"에 대해서 설명드릴께요!', image=img)
        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)
        dispatcher.utter_message(msg3)
        dispatcher.utter_message(msg4)
        buttons = []
        buttons.append({"title": f'동의합니다', "payload": "/last_message"})
        buttons.append({"title": f'동의하지 않습니다', "payload": "/last_message"})
        #response = tracker.get_slot('result') 원하는 부분에 붙여넣기
        dispatcher.utter_message(f'이 설명에 대해서 동의하시나요?(마스터봇질문)', buttons=buttons)

        return [SlotSet('step', 5), SlotSet('is_finished', True)]
import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, unego_get_question
from rasa_sdk.events import FollowupAction



center_leading_step = None
unego_question_intro = "제가 질문 한가지 할게요! 질문을 보시고 솔직하게 답변해주시면 됍니다 :)"

logger = logging.getLogger(__name__)
#추후 밑에 클래스 복사해서 사용
class ActionLeadingCentersIntro(Action):
    def name(self) -> Text:
        return "action_leading_centers_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_intro')
        #기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        definedCnt = 0

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn":"김재헌", "ct":[1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t":3, "p":52}
        print("MetaData: ", metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        is_finished = tracker.get_slot('is_finished')
        if is_finished == True:
            if center_step==0:
                dispatcher.utter_message(
                    f'그럼 센터에 대해 다시 알려드릴게요!'
                )
                dispatcher.utter_message(
                    f'우리 몸에는 9개의 센터가 있으며, 어떻게 당신이 가진 9가지 재능의 힘을 펼칠 수 있는지 알 수 있습니다. 당신의 센터가 정의되어 다른 사람들에게 영향을 미치는 부분과 반대로 다른 사람이나 환경에 의해 영향을 받거나, 관련된 측면에서 다른 사람을 인식할 수 있는 미정의된 센터를 확인할 수 있습니다.')
            else:
                dispatcher.utter_message(
                    f'다음 센터에 대해 알려드릴게요!'
                )
        else:
            if leading_priority[0]==3: #센터에 대한 인트로 추가
                dispatcher.utter_message(
                    f'우리 몸에는 9개의 센터가 있으며, 어떻게 당신이 가진 9가지 재능의 힘을 펼칠 수 있는지 알 수 있습니다. 당신의 센터가 정의되어 다른 사람들에게 영향을 미치는 부분과 반대로 다른 사람이나 환경에 의해 영향을 받거나, 관련된 측면에서 다른 사람을 인식할 수 있는 미정의된 센터를 확인할 수 있습니다.')
                if center_priority[0] == 0: #센터 우선순위중 1순위가 0번째센터면
                    dispatcher.utter_message(
                        f'0번째 센터 인트로')
                elif center_priority[0] == 1:
                    dispatcher.utter_message(
                        f'1번째 센터 인트로')
                elif center_priority[0] == 2:
                    dispatcher.utter_message(
                        f'2번째 센터 인트로')
                elif center_priority[0] == 3:
                    dispatcher.utter_message(
                        f'3번째 센터 인트로')
                elif center_priority[0] == 4:
                    dispatcher.utter_message(
                        f'4번째 센터 인트로')
                elif center_priority[0] == 5:
                    dispatcher.utter_message(
                        f'5번째 센터 인트로')
                elif center_priority[0] == 6:
                    dispatcher.utter_message(
                        f'6번째 센터 인트로')
                elif center_priority[0] == 7:
                    dispatcher.utter_message(
                        f'7번째 센터 인트로')
                elif center_priority[0] == 8:
                    dispatcher.utter_message(
                        f'8번째 센터 인트로')
            else: #인트로도 아니고, 끝난것도 아니면
                if center_step == 0: #즉 중간에 나온 센터인데 그중 첫번째 센터 설명일때
                    dispatcher.utter_message(
                        f'다음으로 센터를 살펴보겠습니다.')
                    dispatcher.utter_message(f'우리 몸에는 9개의 센터가 있으며, 어떻게 당신이 가진 9가지 재능의 힘을 펼칠 수 있는지 알 수 있습니다. 당신의 센터가 정의되어 다른 사람들에게 영향을 미치는 부분과 반대로 다른 사람이나 환경에 의해 영향을 받거나, 관련된 측면에서 다른 사람을 인식할 수 있는 미정의된 센터를 확인할 수 있습니다.')
                else:
                    dispatcher.utter_message(
                        f'다음 센터에 대해 알려드릴게요!.')



        for i in metadata['ct']:
            definedCnt += i

        if leading_priority[0]==3:
            step = 1
        elif leading_priority[1]==3:
            step = 2
        elif leading_priority[2]==3:
            step = 3
        elif leading_priority[3]==3:
            step = 4

        print("center_leading_step", center_leading_step)

        print("get Step")
        print(tracker.get_slot('step'))
        print("center step", tracker.get_slot('center_step'))
        print("get Step end")

        h_center = center_priority[center_step] #센터 몇번째까지 했는지를 기준으로 정하는 부분
        if h_center == 0 and metadata['ct'][0]==1:
            h_type = "연료 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 2 and metadata['ct'][2]==1:
            h_type = "직관 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 3 and metadata['ct'][3]==1:
            h_type = "감정 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 4 and metadata['ct'][4]==1:
            h_type = "에고 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 5 and metadata['ct'][5]==1:
            h_type = "방향 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 6 and metadata['ct'][6]==1:
            h_type = "표현 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 7 and metadata["ct"][7] == 1:
            h_type = "생각 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 8 and metadata["ct"][8] == 1:
            h_type = "영감 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 0 and metadata['ct'][0]==0:
            h_type = "연료 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 1 and metadata['ct'][1]==0:
            h_type = "활력 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 2 and metadata['ct'][2]==0:
            h_type = "직관 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 3 and metadata['ct'][3]==0:
            h_type = "감정 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 4 and metadata['ct'][4]==0:
            h_type = "에고 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 5 and metadata['ct'][5]==0:
            h_type = "방향 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        elif h_center == 6 and metadata['ct'][6]==0:
            h_type = "표현 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 7 and metadata['ct'][7]==0:
            h_type = "생각 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 8 and metadata['ct'][8]==0:
            h_type = "영감 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"

        dispatcher.utter_message(f'{metadata["pn"]}님의 "{h_type}"에 대해서 설명드릴께요!', image=img)
        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)

        buttons = []
        buttons.append({"title": f'네 듣고 싶어요', "payload": "/leading_centers"})
        buttons.append({"title": f'아뇨 괜찮아요', "payload": "/center_unego_question"})

        dispatcher.utter_message(
            f'더 자세히 듣고 싶으신가요?', buttons=buttons)
        return [SlotSet('center_step', center_step), SlotSet('center_type', h_center), SlotSet("step", step)]


class ActionLeadingCenters(Action):
    def name(self) -> Text:
        return "action_leading_centers"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers')
        #기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        definedCnt = 0

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn":"김재헌", "ct":[1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t":3, "p":52}
        print("MetaData: ", metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')

        center_priority = tracker.get_slot('center_priority')

        if leading_priority[0]==3:
            step = 1
        elif leading_priority[1]==3:
            step = 2
        elif leading_priority[2]==3:
            step = 3
        elif leading_priority[3]==3:
            step = 4

        print("center_leading_step", center_leading_step)

        print("get Step")
        print(tracker.get_slot('step'))
        print("center step", tracker.get_slot('center_step'))
        print("get Step end")

        h_center = center_priority[center_step] #센터 몇번째까지 했는지를 기준으로 정하는 부분
        if h_center == 0 and metadata['ct'][0]==1:
            h_type = "연료 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = "항상 자기만의 속도로 일 처리를 하는 당신은 다른 사람들이 일을 빨리 하도록 서두르게 하거나 또는 늦게 하도록 영향을 주는 사람입니다."
            msg2 = "공부든 일이든 또 다른 무언가든 하고있는 것에 대해 ‘끝내야 한다’는 압박을 느껴 스트레스를 받지만 당신은 자기만의 속도로 시작한 것을 끝냅니다. "
            msg3 = "주변에서 아무리 당신을 재촉하거나 늦추도록 압박을 하더라도 아랑곳하지 않습니다. 스트레스는 몸에 쌓입니다. "
            msg4 = "건강한 생활을 하려면 주기적으로 운동 등의 육체적 활동 등을 통해 스트레스를 해소하는 것이 좋습니다.전체 인류의 약 60%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            msg = "항상 몸에 활력 에너지가 있는 당신은 다른 사람들의 지속적인 에너지 사용에 영향을 주는 사람입니다. 자신이 좋아하거나 사랑하는 일을 위해서라면 몇날 며칠을 밤을 새우더라도 그 일이 신이난다면 괜찮을 수 있는 당신은 엄청난 에너지를 지니고 있습니다. "
            msg2 = "이 에너지는 당신이 ‘결정 방식’에 따라 맞게 결정을 했을 때, 몸에서 만들어집니다. 하지만 당신은 대부분 에너지가 없는 상태로 지낼 것입니다. 왜냐하면? 자신의 결정 방식을 따르지 않았기 때문입니다. 그에 따른 결과는 만성피로에 시달리는, 활력없는 당신입니다."
            msg3 = "반면에 자신의 결정 방식을 따라 맞게 결정한 무언가에 대해서는 당신의 몸이 에너지를 만들어낼 것이기 때문에 지치지 않고 계속 할 수 있습니다. "
            msg4 = "몸이 에너지를 낼 수 있는지를 알기위해 주변 사람들에게 “Yes” or ”No”로 답이 가능한 형태의 질문을 받아야 합니다. 그리고 자신의 결정 방식에 따라 맞는 결정을 한다면 당신은 늘 활기찰 수 있습니다. 전체 인류의 약 66%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 2 and metadata['ct'][2]==1:
            h_type = "직관 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = "항상 자신의 직관에 따라 즉흥성을 지닌 당신은 다른 사람들에게 안전감각에 대한 영향을 주는 사람입니다. 몸은 순간순간 변화하는 주변 상황 속에서 당신의 안전을 살피고 있습니다. "
            msg2 = "인식을 할 수도, 그렇지 않을 수도 있지만 당신의 몸은 늘 안전을 살피고 소리나 진동, 냄새, 맛을 통해 안전 또는 위험을 알려줍니다. "
            msg3 = "하지만 직관은 순간적이고 알아차리기 쉽지 않아 놓칠 때도 많고, 알아 차렸는데도 무시되기 쉽습니다. 왜냐하면? 논리적으로 계산하는 생각과 휘몰아치는 감정으로 덮혀 몸에서의 본능을 무시하기 때문입니다. "
            msg4 = "몸이 알려주는 직관에 따른다면 당신은 어떤 상황에서도 안전할 수 있습니다. 전체 인류의 약 55%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 3 and metadata['ct'][3]==1:
            h_type = "감정 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = "항상 자신의 직관에 따라 즉흥성을 지닌 당신은 다른 사람들에게 안전감각에 대한 영향을 주는 사람입니다. 몸은 순간순간 변화하는 주변 상황 속에서 당신의 안전을 살피고 있습니다. "
            msg2 = "인식을 할 수도, 그렇지 않을 수도 있지만 당신의 몸은 늘 안전을 살피고 소리나 진동, 냄새, 맛을 통해 안전 또는 위험을 알려줍니다. "
            msg3 = "하지만 직관은 순간적이고 알아차리기 쉽지 않아 놓칠 때도 많고, 알아 차렸는데도 무시되기 쉽습니다. 왜냐하면? 논리적으로 계산하는 생각과 휘몰아치는 감정으로 덮혀 몸에서의 본능을 무시하기 때문입니다. "
            msg4 = "몸이 알려주는 직관에 따른다면 당신은 어떤 상황에서도 안전할 수 있습니다.전체 인류의 약 55%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 4 and metadata['ct'][4]==1:
            h_type = "에고 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = "항상 의지력이 있는 당신은 다른 사람들의 가치와 자존감에 영향을 주는 사람입니다. 다른 사람들이나 다른 무언가는 모두 경쟁하여 이겨야할 상대입니다. "
            msg2 = "당신은 의지력이 있는 사람이고, 의지력을 통해 세상의 다양한 것들과 경쟁합니다. 경쟁을 통해 비교 우위에 서려는 당신은 스스로 그렇게 생각하든 그렇지 않든 자연스러운 자존감에 대한 감각이 있습니다. "
            msg3 = "‘나 이런 사람이야!! 나 잘난 사람이야!! 내가 이것도 못할 것 같아?’ 라고 생각합니다. 그리고 의지력을 발휘해 하고자 한 것을 이루어내기도 합니다. 이러한 당신은 때때로 “왜 너는 못하니? 왜 이렇게 약하니?” 라고 말하며 다른 사람들을 압박할 수 있습니다. "
            msg4 = "모두가 당신처럼 할 수 있는 것은 아니란 것을 반드시 이해하고 알아야 합니다. 전체 인류의 약 37%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 5 and metadata['ct'][5]==1:
            h_type = "방향 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = "항상 자기만의 방향성에 따라 삶을 살아가는 당신은 다른 사람들의 사랑, 방향, 정체성에 영향을 주는 사람입니다. 자기만의 방향성이 있는 것은 하나의 길을 가는 것과 같으며 한 사람이나 한 가지 일을 꾸준히, 오래도록 좋아하는 것과도 같습니다. "
            msg2 = "이것은 당신 인생의 목표라고 볼 수도 있습니다. 자신의 방향성에 대해 알고 계신가요? 목표에 대해서는요? 그것을 알든 모르든 당신은 자기만의 방향성에 따라 하나의 길을 꾸준히 걸어왔고, 또 꾸준히 가고 있을 것입니다. "
            msg3 = "사람에 대해서나 일에 대해서나 신념에 대해서 자주 변하지 않는 일관성 있는 사람이라도 할 수도 있습니다. 지나온 삶을 돌아보았을 때, 지나온 길에서 했던 여러 경험들은 어떤 하나의 목표를 향하고 있지 않았나요? 당신의 방향성은잘 바뀌지 않습니다."
            msg4 = "때때로 다른 사람들을 자신이 옳다 생각하는 방향으로 이끌려고 하거나 강요할 수 있으니, 이 점을 유의하셔야 합니다. 전체 인류의 약 57%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 6 and metadata['ct'][6]==1:
            h_type = "표현 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = "항상 자기만의 방식으로 말하고 행동하는 당신은 다른 사람들의 표현방식에 영향을 주는 사람입니다. 자기만의 방식으로 말하고 행동하는 당신은 자기만의 표현방식이 있습니다. "
            msg2 = "늘 같은 방식으로 말이나 행동을 하기 때문에 이것은 자기만의 목소리, 표현방식이 있는 것입니다. 당신은 말이나 목소리 혹은 행동을 함으로서 사람들의 이목을 끕니다."
            msg3 = "때때로 당신은 지나치게 많은 말이나 행동으로 인해 다른 사람들에게 반감을 일으킬 수도 있습니다. 표현은 다른 사람들, 즉 세상과의 소통을 위한 것입니다. "
            msg4 = "어떤 표현이든 맞는 장소에서 맞는 때에 맞는 말을 적당이 하는 것이 필요합니다. 전체 인류의 약 72%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 7 and metadata["ct"][7] == 1:
            h_type = "생각 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7.gif"
            msg = "항상 자기만의 방식으로 생각하고 개념화하는 당신은 다른 사람들의 사고방식에 영향을 주는 사람입니다. 생각하고 의견을 내는데에 있어서 당신은 일정한 방식이 있습니다. "
            msg2 = "도표나 그림을 떠올리며 생각을 하기도 하고, 어떤 소리가 들려와 생각하기도 하고, 과거에 했던 경험을 바탕으로 생각을 하는 등의 과정을 거쳐 자기만의 의견을 가지게 됩니다. "
            msg3 = "이렇게 형성된 당신의 의견은 좀처럼 바뀌지 않고, 외부의 영향에도 잘 흔들리지 않습니다. 자기 신념이 확고한 것이라고 할 수 있습니다. "
            msg4 = "또한 당신은 무언가를 이해하려 집착적으로 생각하다가 근심에 휩싸일 수 있지만 생각은 생각일 뿐, 행동은 하시면 안됩니다. 전체 인류의 약 47%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 8 and metadata["ct"][8] == 1:
            h_type = "영감 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8.gif"
            msg = "항상 머릿속에 떠오르는 의문에 대한 답을 찾는 당신은 다른 사람들이 무언가에 대해 생각하도록 영감을 주는 사람입니다. "
            msg2 = "때때로 과거의 경험이 떠올라 혼란스러울 수 있고(‘도대체 그 일이 왜 자꾸 떠오르지?’), 무언가에 대한 의심이 들고(‘어? 이거 뭔가 이상한데? 뭔가 안맞는데?’), 알듯 말듯한 것을 명확히 알고싶겠지만(‘이게 뭘까? 뭐지? 알 것도 같은데..’) "
            msg3 = "이것은 단지 당신이 세상을 이해하기 위한 현상이라는 사실을 알아야 합니다. 억지로 답을 찾으려는 노력을 하는 동안에는 답이 보이지 않고, 답을 찾기를 멈추었을 때, 답을 보게 될 것입니다. "
            msg4 = "전체 인류의 약 30%가 이 에너지를 고정적으로 가지고 있습니다."
        elif h_center == 0 and metadata['ct'][0]==0:
            h_type = "연료 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            msg = "다른 사람이나 다른 무언가로부터 ‘빨리 끝내야한다’는 압박을 받는 당신은 자신을 움직이게 하거나 멈추게하는 압박을 필요에 따라 이용할 수 있는 사람입니다. 공부든 일이든 또 다른 무언가든 하고있는 것에 대해 ‘빨리 끝내야한다’는 압박을 느끼면 엄청나게 급해져서 서두릅니다. "
            msg2 = "지나친 압박은 지나친 스트레스가 되어 당신을 힘들게 합니다. 걸어다녀도 되는데 급히 뛰다가 넘어지거나 책상이나 자리에 천천히 앉아도 되는데 서둘러 앉다가 자주 부딪히거나, 손에 든 물건이나, 주머니에 넣어둔 물건을 급히 꺼내다가 자주 떨어트리진 않나요? "
            msg3 = "여러 사람이 모인 자리나 강의같은 장소에서 가만히 있는 것이 힘든가요? 시간이 충분히 주어진 일을 서둘러서 일찍 끝내느라 조급한가요? 이것은 자기자신으로부터 출발한 것이 아닌, 외부에서 들어온 조건화의 영향으로 인한 것입니다. ‘빨리 가야해. 서둘러야해. 가만히 있으면 안돼. 빨리 끝내야해.’ 라는 생각이 들어 조급해 질 때를 잘 알아차리고 속도를 늦출 필요가 있습니다."
            msg4 = "빨리 가지 않아도 되고 서두르지 않아도 되며, 가만히 있어도 됩니다. 그리고 서둘러서 급히 끝내야 하는 것도 없습니다. 전체 인류의 약 40%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 1 and metadata['ct'][1]==0:
            h_type = "활력 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 오는 활력 에너지에 열려있는 당신은 에너지 효율에 대한 아이디어가 있는 사람입니다. 더 일하고, 더 공부하고, 더 놀고, 더 자고, 더 먹고 등등. 당신은 늘 아쉽습니다. 더 해야할 것 같고, 더 했으면 좋겠는데 생각과 달리 체력이 따라주지 않습니다. "
            msg2 = "그럼에도 늘 ‘더 하고 싶어!! 더 할거야!!!’ 라고 생각하며 늘 지나치게 무언가를 합니다. 자신에게는 활력 에너지가 없는데도 마치 가지고 있는 것처럼 착각하는 것입니다. 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. 이로 인해 당신은 모든 것에 있어서 충분한 때를 모릅니다. "
            msg3 = "그래서 지나치게 무언가를 하고 몸에 무리가 와 힘들어하기 쉽습니다. 밖에서는 힘차게 있다가 집으로 돌아오면 극심한 피로를 느끼며 지쳐 쓰러지듯 잠드는 것이 자신의 모습이라면, 주의해야합니다. 계속해서 무리하게 에너지를 쥐어짜며 살다가는 자기 자신의 건강을 해치기 쉽기 때문입니다. "
            msg4 = "당신은 활력 에너지를 통해 생산적인 일을 하는 사람이 아닙니다. 절대 무리하지 말고, 되도록 많이 많이 쉬어야 합니다. 전체 인류의 약 34%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 2 and metadata['ct'][2]==0:
            h_type = "직관 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 안전 감각에 대한 영향을 받는 당신은 ‘누가 건강하고, 누가 건강하지 않은지’를 잘 알 수 있는 사람입니다. 평소에 혼자 있을 때 당신은 몸의 느낌이 썩 좋지 않습니다. 몸이 아픈 것 같은, 어딘가가 허한, 마치 텅 빈 느낌입니다. "
            msg2 = "그러다가 다른 사람들과 있게되면 아팠던 것 같은 몸의 느낌이 좋아지며, 안정감마저 듭니다. 그래서 당신은 이러한 느낌을 주는 사람이나 다른 무언가에 매달립니다. 친구나 가족 연인과 연락이 안되면 수십 번 연락을 했던 경험 있습니까? ‘무슨 사고가 났나? 왜 연락이 안되지? 혼자 있으면 죽을 것 같아. '어쩌지~어쩌지~' 라는 생각과 느낌으로 인해 안절부절 못하고 시달립니다."
            msg3 = "때로는 옳지 않은 관계나 사람에게서도 벗어나지 못하고 매달릴 수도 있습니다. 마치 술이나 담배처럼 사람관계에 있어서도 중독되어 버리는 것입니다. 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. 이로 인해 당신은 위와 같은 현상을 겪을 수 있고 힘들어질 수 있기 때문에 유의해야 합니다. "
            msg4 = "무언가에 매달려있는 당신, 지금 이대로 괜찮습니까? 당신에게는 어떤 사람이 건강한지, 무엇이 안전한지를 잘 구별할 수 있는 잠재성이 있습니다. 전체 인류의 약 45%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 3 and metadata['ct'][3]==0:
            h_type = "감정 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 오는 다양한 감정에 열려있는 당신은 누가 감정적으로 성숙한지를 잘 알 수 있는 사람입니다. 혼자 있을 때, 거의 대부분 감정적으로 평온하지만 다른 사람들과 있게되면 반드시 타인의 감정의 영향을 받습니다. "
            msg2 = "상대방이 기쁘면 더 기쁘고, 상대방이 슬프면 더 슬프고, 상대방이 화나면 더 화가 나는게 당신입니다. 당신은 TV나 영화를 보면서도 주인공의 감정이나 스토리에 더 울고 웃습니다. 당신은 늘 ‘저 사람 기분 괜찮나? 화났나? 분위기 왜 이러지?’ '이걸 말해도 괜찮을까?' 등등 타인의 느낌이나 감정상태에 매우 예민 할 수 있습니다. "
            msg3 = "그리고 상대방으로부터 부정적인 감정이 느껴진다면, 그 사람이나 상황을 피하고 싶어집니다. 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. 만일 피치못할 상황이 되어 당신이 화가 난다면 당신은 매우 흥분이 되어 화를 낼때 손끝이 시릴 정도로 차가워지거나 온 몸이 벌벌 떨릴 정도로 부들부들 떨기도 하며, 말도 꼬일 정도로 화가 나는 것을 경험할 수 있습니다. "
            msg4 = "이런 상황은 다른 사람들에게 보이는 것보다 당신에겐 매우 힘든 것이므로, 당신은 ‘좋은게 좋은거다.’라는 태도로 일관하며 부딪치지 않을 수도 있습니다. 그런데 정말 부딪치지 않으면 다 괜찮을 것 일까요? 당신이 심하게 느끼는 감정적 불안감은 자신의 것이 아닌, 다른 사람들의 감정이라는 사실을 알아야 합니다. 전체 인류의 약 47%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 4 and metadata['ct'][4]==0:
            h_type = "에고 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 오는 자존감에 대한 감각에 열려있는 당신은 누가 건강한 자존감을 보이는지 잘 알 수 있는 사람입니다. 지나치게 낮은 자존감으로 인해 문제를 겪든, 지나치게 높은 자존감으로 인해 착각에 빠져있든, ‘자존감’을 표현하려고 하거나, 뭔가 입증을 하려고 하는 것 자체는 당신과는 전혀 관계가 없습니다. "
            msg2 = "자존감이 낮을 때는 자기비하에 빠져 허우적대고 문제라고 생각하면서 어떻게든 자존감을 끌어올리려고 합니다. 자존감이 지나치게 높을 때는 착각에 빠져 자신이 잘났다는 것을 끊임없이 주변에 어필하여 사람들의 눈살을 찌푸리게 합니다. "
            msg3 = "이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향임을 알아야 합니다. 이로 인해 당신은 위와 같은 현상을 겪을 수 있지만. 이는 문제가 아닙니다. 하지만 이를 문제로 여길 때, 당신은 끊임없이 자신을 다른 사람이나 다른 무언가와 비교하며 더욱 더 괴로워질 것입니다. 그러나 그럴 필요가 없습니다. "
            msg4 = "당신은 다른 누구보다, 다른 무엇보다 잘나기 위해 입증을 해 보여야 하는 사람이 아닙니다. 전체 인류의 약 63%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 5 and metadata['ct'][5]==0:
            h_type = "방향 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = "다른 사람이나 다른 무언가로부터 사랑, 방향, 정체성에 대한 영향을 받는 당신은 삶에서 다양한 사랑, 방향, 정체성을 경험하는 사람입니다. 삶에는 다양한 방향이 존재합니다. 당신이 스스로 그렇다는 것을 알든 모르든, 방향, 즉 어디로 가야할지 모르겠는 당신은 하나의 길만을 가는 사람이 아닙니다. "
            msg2 = "방향은 늘 변하고, 목적지를 알지 못해도 당신은 어디로든 가고는 있습니다. 변화는 늘 불안감을 가져오기 때문에 당신은 하나의 목표, 한 길만을 가려고 합니다. 또한 누구와 있느냐에 따라 달라지는 자신을 보면서 ‘내가 누구지? 나는 왜 자꾸 변하지?’라는 의문이 들어 혼란스럽습니다. "
            msg3 = "그래서 ‘나는 누구인가?’라는 의문에 대한 답을 찾아 이리저리 돌아다니기도 합니다. 하지만 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향 조건화입니다. 이로 인해 당신은 위와 같은 현상을 겪을 수 있지만. 이는 문제가 아닙니다. "
            msg4 = "당신은 다양한 사람들의 사랑, 방향, 정체성을 경험하는 것을 통해 지혜로워질 잠재성이 있습니다. 전체 인류의 약 43%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 6 and metadata['ct'][6]==0:
            h_type = "표현 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 말과 행동에 대한 압박을 느끼는 당신은 누가 진실을 말하고, 누가 거짓을 말하는지 잘 알 수 있는 사람입니다. 사람들의 관심을 받고싶어 지나치게 말하거나 이상한 행동을 하신 적이 있습니까? 이목을 끌고싶은 당신은 ‘관종(관심종자)’의 끼가 다분합니다. "
            msg2 = "말과 행동의 방식이 일관되지 않은 당신은 말이나 행동을 할 때 불안감에 휩싸이기도 합니다. ‘무슨 말이든 해야할 것 같은데? 무슨 말을 해야하지? 가만히 있어도 되나?’ 라는 생각을 하며 말과 행동에 대한 압박을 느끼기 때문에 계속 말하고, 지나치게 말하고, 아무 말이나 하는 것입니다. "
            msg3 = "이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. 이로 인해 당신은 위와 같은 현상을 겪을 수 있고, 다른 사람들과의 소통에 있어서 힘들어질 수 있기 때문에 지나친 말과 행동에 유의해야 합니다. 당신이 먼저 말을 시작하기 보다는 가능한 다른 사람들이 당신에게 말을 걸었을 때, 얘기를 시작하는 것이 좋습니다."
            msg4 = "당신은 다양한 방식으로 표현을 할 수 있으며, 누구의 말이 더 신뢰할 수 있는지를 잘 구별할 수 있는 잠재성이 있습니다.전체 인류의 약 28%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 7 and metadata['ct'][7]==0:
            h_type = "생각 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7_off.png"
            msg = "다른 사람이나 다른 무언가로 부터 오는 다양한 사고방식에 열려있는 당신은 정보를 스폰지 처럼 흡수하는 사람입니다. 다양한 사고방식에 열려있는 당신은 사람, 책, 미디어 등 모든 것에서 오는 다양한 정보들이 흥미롭습니다. ‘이런 의견도 있구나. 저렇게 생각할 수도 있겠는데? 이 정보도 일리가 있어.’ 라고 생각합니다. "
            msg2 = "하지만 다른 한 편으로는 ‘나는 왜 다 일리가 있다고 할까? 왜 자꾸 생각이나 의견이 바뀌지? 귀가 얇은가?’ 라는 생각도 듭니다. 흔히 말하는 팔랑귀, 그것이 바로 당신의 건강한 모습입니다. 팔랑귀라고 해서 무조건 나쁜 것이 아닙니다."
            msg3 = "이것을 문제로 여기기 시작할 때, 다양한 생각과 의견에 대한 당신의 열린 자세는 닫힌 자세로 바뀌어 특정 생각이나 의견에 자신을 묶어버립니다. 그리고 자신의 생각과 의견만이 맞다고 합니다. 아주 고집스러워지는 것입니다. 영원히 바뀌지 않을 생각과 의견이 세상에 존재하기는 할까요? "
            msg4 = "당신에게는 어떤 생각이 더 좋은 것이고, 어떤 의견이 더 맞는 것인지 잘 구별할 수 있는 잠재성이 있습니다.전체 인류의 약 53%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 8 and metadata['ct'][8]==0:
            h_type = "영감 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8_off.png"
            msg = "다른 사람이나 다른 무언가로부터 영감을 받는 당신은 ‘누가 나에게 혼란을 주고, 누가 나에게 영감을 주는지’를 잘 알 수 있는 사람입니다."
            msg2 = "평소에 생각이 많지 않다가 어떤 때에는 지나치게 생각이 많아져서 머리가 지끈거리거나, 생각을 하고 또 하고 또 하다가 불면증에 시달린 경험들 있습니까? 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. "
            msg3 = "이로 인해 당신은 위와 같은 현상을 겪을 수 있지만 이는 당신의 문제가 아닙니다. 또한 각종 영화, 드라마, 콘서트, 책, 강의, 전시회 등 영감을 주는 재미있는 것들을추구하게 되기 때문에 ‘오, 이거 재미있을 것 같아. 이건 나에게 영감을 줄것 같아. 이건 해야해!! ’라는 생각을 하며 온갖 것들을 합니다."
            msg4 = "온갖 영감을 받기위해 했던 많은 것들이 모두 당신에게 영감을 주었나요? 당신에게는 혼란과 영감을 잘 구별할 수 있는 잠재성이 있습니다. 전체 인류의 약 70%는 이 센터가 정의되어 있지 않습니다."

        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)
        dispatcher.utter_message(msg3)
        dispatcher.utter_message(msg4)

        return [SlotSet("is_question", 0), SlotSet("center_type", h_center), SlotSet("center_step", center_step),
                SlotSet("center_question", True), SlotSet("step", step), SlotSet("is_sentiment", True),
                FollowupAction(name="action_center_unego_question")]

class ActionLeadingCentersQuestion(Action):
    def name(self) -> Text:
        return "action_leading_centers_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_question')

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn":"김재헌", "ct":[1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t":3, "p":52}
        print("MetaData: ", metadata)
        step = tracker.get_slot('step')

        return [SlotSet('step', step), SlotSet("center_question", False), FollowupAction(name='action_more')]

class ActionCenterUnegoQuestion(Action):
    def name(self) -> Text:
        return "action_center_unego_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_center_unego_question')
        # metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "se": [2, 0, 6], "t": 3, "p": 52}
        center_type = tracker.get_slot("center_type")
        center_step = tracker.get_slot("center_step")
        step = tracker.get_slot("step")
        print(step)
        unego_question = ''
        if metadata['ct'][center_type] == 0:
            unego_question = unego_get_question(center_type, defined=False)
        else:
            unego_question = unego_get_question(center_type, defined=True)

        dispatcher.utter_message(unego_question[0])
        dispatcher.utter_message(unego_question[1])
        center_step +=1
        return [SlotSet('bot_question', unego_question[1]), SlotSet("is_question", 0),
                SlotSet("center_type", center_type), SlotSet("center_step", center_step),
                SlotSet("center_question", True), SlotSet("step", step), SlotSet("is_sentiment", True)]

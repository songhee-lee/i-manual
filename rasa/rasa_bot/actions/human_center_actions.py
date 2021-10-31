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
                        f'당신은 인류의 28%에 해당하는 특별한 사람입니다.')
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
            msg = "인류의 60%는 연료센터에서 자신만의 에너지를 발신하며 다른 사람들이 내뿜는 압력에 좌우되지 않고 자신의 고유한 페이스대로 나아갈 수 있는 능력을 갖고 있습니다. 당신은 바로 이러한 부류의 사람입니다. 즉, 자신만의 스트레스를 원동력 삼아 세상에 없는 새로운 무엇인가를 만들러 온 사람들이라고 할 수 있습니다."
            msg2 = "연료센터는 3개의 다른 센터와 연결되어 있습니다. 직관센터와 연결되어 있다면 자신만의 정해진 방식으로 스트레스를 사용하여 삶의 잘못된 것들을 고치기 위해 애씁니다. 생존 자체를 위해 연료를 사용하고 그것을 통해 살아있음의 기쁨과 즐거움을 느낍니다."
        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 2 and metadata['ct'][2]==1:
            h_type = "직관 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = "당신은 갖고 태어난 능력은 오직 지금 이 순간에만 적용되며 말로는 표현할 수 없는 내면적 인식입니다. 직관(직감)이라는 것은 특히 생명에 직결되고 즉흥적으로 일어나는 정보인데 예를들면 “느낌이 쎄-해”, “그냥 내 촉이 그래”와 같은 느낌입니다. 주의할 점은 직관센터는 한 번 경고를 주고 나면 다시 알려주지 않는다는 점입니다. 처음 직관에서 경고를 했을 때, 그것을 합리화하려는 생각이나 외부의 주변 분위기에 맞춰서 타협 혹은 미룰 경우 기회를 놓치게 됩니다."
            msg2 = "직관센터가 정의되어 있는 당신은, 더더욱 내면에 귀를 기울이고 그 경고를 무시해서는 안됩니다. 경고를 무시할수록 당신은 자신의 건강을 잃게 됩니다. 직관센터의 경고를 신뢰하고 존중할 경우, 선천적인 면역력과 건강을 기반으로 나의 삶에서 위험요소들을 줄일 수 있습니다."

        elif h_center == 3 and metadata['ct'][3]==1:
            h_type = "감정 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = "인류의 절반은 자신만의 감정 에너지를 갖고 발신하며 살고 있고, 나머지 절반은 특별한 감정 에너지 없이 다른 절반이 발신하는 감정 에너지에 영향을 받으며 살아가고 있습니다. 이러한 감정 에너지와 관련된 센터를 감정센터라고 부릅니다. 감정센터가 정의되어 있는 사람들은 자신만의 감정 에너지의 사이클을 갖도록 디자인된 사람들입니다."
            msg2 = "당신은 감정센터가 정의되어 있는 사람에 속하므로 자신만의 고유한 감정 에너지의 사이클을 가지며 항상 감정의 업과 다운이 존재함을 느낍니다. 당신에게 인내심을 요구하는 것은 쉬운 일이 아닙니다. 당신은 늘 자신의 감정파도 속에서 파도가 높으면 상기되어 고조된 채로 쉽게 결정을 내려버리고, 파도가 낮으면 가라앉은 채로 아무것도 하지 않으려는 무기력한 모습을 보이기 쉽습니다."

        elif h_center == 4 and metadata['ct'][4]==1:
            h_type = "에고 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = "에고센터는 무언가를 하고 싶은 의지, 용기, 그리고 경쟁을 통해 성취해내는 에너지와 관련된 센터입니다. 이 센터가 정의되어 있는 사람들은 인류의 37% 정도이며 이러한 에너지를 계속 발신하면서 자신만의 의지와 용기로 세상과 맞서 싸우며 살아갑니다. 당신은 에고센터 정의에 해당하므로 이렇게 살아가도록 디자인되어 있습니다."
            msg2 = "당신이 무엇을 입을지, 어디서 일할지, 몇시간이나 일을 할지, 일을 처리하기 위해 시간이 얼마나 필요한지 모든 것을 스스로 통제하고 결정하고 싶어 합니다. 스스로의 가치를 잘 알고 있고 약간은 자신감을 과장하는 경향도 있습니다."

        elif h_center == 5 and metadata['ct'][5]==1:
            h_type = "방향 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = "당신은 당신의 방향센터에서 에너지를 발신하는 사람입니다. 이것을 방향센터 정의라고 부릅니다. 이러한 부류의 사람들은 사랑 받는다는 게 어떤 느낌인지, 사랑을 주는게 어떤 것인지 자신만의 감각을 가지고 있습니다. 자기자신을 아끼고 스스로를 사랑하며 그와 같이 다른 사람들에게도 사랑을 전합니다."
            msg2 = "삶에서 나의 길이 어디를 향하는지 내가 가야 할 방향을 알고 새로운 길을 개척하는 것도 어려움이 없습니다. 어디로 가야 하는지 길을 잃은 듯한 다른 사람들에게 안정감을 줄 수도 있고, 더 나아가 인류가 어느 방향을 향해야 하는지 진화하기 위한 길이 무엇인지 전하는 역할을 할 수도 있습니다."

        elif h_center == 6 and metadata['ct'][6]==1:
            h_type = "표현 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = "당신은 표현센터를 통해 자신만의 고유한 표현방식으로 자신이 원하는 때에 하고 싶은 말이나 표현을 할 수 있는 능력을 타고난 사람입니다. 이것을 표현센터가 정의되어 있다고 말합니다. 표현센터는 당신을 구성하는 9개의 센터 중 중심점이고 당신이 가진 모든 것을 모아 당신의 내면을 외부세상에 표현하고 행동하도록 해줍니다."
            msg2 = "무슨 말을 해야 할 지, 어떻게 전달해야 할 지, 언제 표현하는 것이 좋을지, 자신만의 감각을 가지고 있습니다. 하지만 자신만의 감각을 가지고 있는 것이 꼭 좋은 것만은 아닙니다. 표현센터가 어떤 센터에 연결되어 있냐에 따라 다양한 상황이 만들어지기 때문입니다."
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
            msg = "누구나 갖고 있는 9개의 센터 중에서 연료센터는 우리 몸에 주어지는 육체적 압박감에 대한 에너지와 관련이 있습니다. 당신은 인류의 40%에 해당하는 연료센터가 정의되어 있지 않은 부류에 해당합니다. 연료센터는 우리 몸의 아드레날린과 관련이 있는데 연료센터가 미정인 당신은 이것이 꾸준하지 않기 때문에 한 번 일을 시작해도 그것을 오래도록 이어가진 못합니다. 그러다보니 한가지를 진득하게 하기보다는 이것하다 저것하다 분주하기만 하기 쉽죠. 초점이 없이 여러가지에 바쁘기만 합니다."
            msg2 = "당신은 주변의 모든 일을 자신이 받아서 하려고 나서거나 해결할 수 없는 압박감을 해결하기 위해 바쁘곤 합니다. 그러다보면 결국에는 탈진하거나 번아웃되어 질려버리고 말죠. 자각하지 못한채 외부로부터 들어오는 압박에 의해 자신이 작동되도록 내버려두게 됩니다. 당신이 느끼는 대부분의 압박감은 당신 자신의 것이 아니라는 것을 자각하기 바랍니다."
        elif h_center == 1 and metadata['ct'][1]==0:
            h_type = "활력 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            msg = "센터 간단한 설명입니다"
            msg2 = "앞부분 설명"
        elif h_center == 2 and metadata['ct'][2]==0:
            h_type = "직관 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = "인류의 45%는 생존에 대한 두려움이나 불안감에 대한 감각이 거의 없습니다. 반면 나머지 55%는 본능적으로 생존에 대한 위협에 대한 자신만의 감각을 지니고 있습니다. 이러한 역할을 담당하는 센터를 직관센터라고 부르고 당신이 속한 45%의 부류를 직관센터가 정의되어 있지 않다, ‘직관센터 미정’이라고 말합니다. 즉, 당신의 직관센터는 에너지를 발신하지 않으므로 두려움이나 불안감에 대해 별다른 감각을 갖고 있지 않고, 건강한 상태의 직관센터 미정이라면 오히려 이러한 부분에 대해 편안함을 느끼며 살게 됩니다."
            msg2 = "하지만 우리의 삶은 늘 다른 사람들과의 관계속에서 이루어지므로 나머지 55%의 사람들이 발신하는 에너지들이당신과 같은 미정들에게도 영향을 미치게 됩니다. 즉, 당신 자신은 별다른 두려움이나 불안감이 없음에도 가까운 사람이 발신하는 에너지를 받거나 심지어 증폭하여 두려움과 불안감을 느끼게 될 수 있습니다."

        elif h_center == 3 and metadata['ct'][3]==0:
            h_type = "감정 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = "인류의 절반은 자신만의 감정 에너지를 갖고 발신하며 살고 있고, 나머지 절반은 특별한 감정 에너지 없이 다른 절반이 발신하는 감정 에너지에 영향을 받으며 살아가고 있습니다. 이러한 감정 에너지와 관련된 센터를 감정센터라고 부릅니다. 감정센터가 정의되어 있는 사람들은 자신만의 감정 에너지의 사이클을 갖도록 디자인된 사람들입니다."
            msg2 = "나머지 절반의 사람들은 감정센터 미정으로 자신만의 감정 에너지를 발신하지 않고 주변에서 발신하는 감정 에너지의 영향을 받게 됩니다. 물론 좋은 감정 에너지의 발신은 감정센터 미정들에게도 너무나 큰 행복감을 줄 수 있습니다. 당신은 감정센터 미정에 속하는 사람이므로 늘 다른 사람들의 감정 에너지 흐름에 민감하고 그것에 좌우되는 경우가 많습니다."

        elif h_center == 4 and metadata['ct'][4]==0:
            h_type = "에고 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = "에고센터는 무언가를 하고 싶은 의지, 용기, 그리고 경쟁을 통해 성취해내는 에너지와 관련된 센터입니다. 이 센터가 정의되어 있는 사람들은 인류의 37% 정도이며 이러한 에너지를 계속 발신하면서 자신만의 의지와 용기로 세상과 맞서 싸우며 살아갑니다. 하지만 당신이 속한 63%의 사람들은 이러한 경쟁의 부담감으로부터 자유로운 사람들입니다. 다른 사람들에게 무엇을 해주어 나의 가치를 인정받고 싶다거나, 내가 무엇인가를 성취하여 나의 존재를 드러내고 싶다거나, 지금의 이 경쟁에서 이겨내고 싶다는 부담을 전혀 느낄 필요가 없는 사람들입니다."
            msg2 = ""

        elif h_center == 5 and metadata['ct'][5]==0:
            h_type = "방향 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = "당신은 고정된 정체성을 갖기 보다는 어느 환경, 어느 자리에서든 자유롭게 자기 자신을 녹여낼 수 있는 특징을 갖고 있습니다. 당신은 자신만의 방향성을 갖고 있기 보다는 다른 사람들의 영향력에 의해 여기저기로 항하게 되며 그러한 과정을 거치면서 자신의 방향으로 점차 맞춰나갑니다."
            msg2 = "여기저기를 경험하는 동안 자신만의 정체성을 쌓아가며 자신만의 아지트, 집중할 수 있는 곳, 즐겨가는 단골가게 등을 만들어갑니다. 이러한 모든 것들이 모여 당신의 방향을 만들어줍니다."

        elif h_center == 6 and metadata['ct'][6]==0:
            h_type = "표현 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = "당신은 자신의 의견을 말하거나 뭔가를 표현하기 위해 애쓰지 않아도 다른 사람들의 주의를 자연스럽게 끌게 되고 초대받게 되는 에너지를 갖고 있습니다. 이렇게 초대되어질 때 가장 자연스럽게 주의가 모아지고, 가장 좋은 타이밍에, 가장 힘들이지 않고, 제일 효과적인 반응을 이끌어낼 수 있습니다."
            msg2 = "억지로 고민하며 말을 하려고 하지도 말고, 침묵의 불편함이 싫어서 불필요한 말을 할 필요도 없고, 뭔가 의견이나 표현이 떠오르면 떠오르는 대로 자연스러운 모습 그대로 있는 것이 좋습니다. 통제하지 않는, 자유로운 목소리가 당신의 진정한 모습입니다."
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


        return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                SlotSet("step", step), FollowupAction(name='action_center_detail_intro')]


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
        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        h_center = center_priority[center_step] #센터 몇번째까지 했는지를 기준으로 정하는 부분
        if h_center == 0 and metadata['ct'][0]==1:
            h_type = "연료 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = "당신의 연료센터가 감정센터와 연결될 경우 개인적 혹은 대인 관계에서의 감정적 스트레스에 대해 스스로의 방식으로 해소할 수 있습니다. 감정적 스트레스를 극복하는 과정을 통해서 더욱 감정에 성숙해지고 다채롭게 드러낼 수 있게 됩니다."
            msg2 = "연료센터와 연결될 경우, 지나치게 스트레스에 노출되어 강박적인 성향을 가질 수 있습니다. 모든 스트레스에 무차별적으로 과민 반응하며 건강을 축낼 수 있습니다. 이러한 경우 자신의 스트레스를 주변으로 퍼트리지 않도록 주의하기 바랍니다."

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
            msg = "세상에는 직관센터가 정의되어 있는 당신과 같은 부류의 사람들이 55%, 나머지 45%의 사람들은 직관센터가 미정입니다. 즉, 당신과 같은 생존에 대한 직관이 존재하지 않습니다. 따라서, 직관센터 미정인 사람들에게는 직관센터가 정의된 사람이 옆에 함께 있어주는 것만으로도 기분이 좋고 건강이 낫는 것 같은 영향을 주기도 합니다."
            msg2 = "당신의 직관센터 에너지가 건강하게 작동할 경우 삶에서 맞닥뜨릴 수 있는 위험요소에 대한 걱정과 두려움은 고민할 필요도 없으며, 그 결과 자연적으로 실존 그 자체를 깊이 경험할 수 있습니다. 초 단위로 작동하는 직관센터의 면역체계가 당신을 지켜줍니다."

        elif h_center == 3 and metadata['ct'][3]==1:
            h_type = "감정 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = "감정대로 결정을 내리면, 안좋은 일을 Yes 해버리거나 좋은 일을 No 해버리는 경우가 많다는 걸 경험해 보았을거예요. 당신의 감정 사이클이 높지도 않고 낮지 않은 평정심일 때 중요한 결정을 하는 것이 매우 중요합니다. 당신의 감정이 어떠한지 알 수 있는 유일한 방법은 그 감정의 파도가 지나간 후에 아까 내가 어떤 상태였구나 (높은 파도였구나, 낮은 파도였구나) 라는 것을 스스로 알아차리는 수 밖에는 없습니다. "
            msg2 = "감정센터의 에너지는 달콤하고, 유혹적이며 강력합니다. 오직 자신의 감정의 흐름만 인내하고 지켜볼 수 있다면 얼마든지 자신에게 유리하게 사용할 수 있다는 겁니다. 당신이 감정적으로 명료하게 결정을 내리기 위해 인내하는 시간은 자연스레 다른 사람들에게도 똑같은 기다림의 시간이 되며, 그 기다림의 시간동안 그들은 결국 당신의 그 에너지를 그 따스함을 더욱 원하게 됩니다. "

        elif h_center == 4 and metadata['ct'][4]==1:
            h_type = "에고 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = "당신은 일하는 것을 즐기는 편이고, 당신 스스로가 모든 것을 통제하고 결정할 수 있을 때 가장 자연스럽고 내면의 힘을 발휘할 수 있습니다. 자신의 목표한 것, 약속한 것을 지켜내는 과정을 즐기고, 주변 사람들에게도 그러한 과정을 즐기도록 영향력을 발휘합니다. 자신의 내면에 귀 기울일 때 의지력은 더욱 온전히 발휘되고 일과 휴식의 균형뿐만 아니라 상황에 맞는 가장 적합한 해결책을 보여줍니다."
            msg2 = "하지만, 누군가에 의해 무시되거나 거절되어 당신 에고의 의지력이 억눌릴 경우 건강에 안좋은 영향을 미칩니다. 따라서, 무작정 의지력만 믿고 이것 저것 일을 벌리거나 실현 가능성이 없는 허무맹랑한 약속만 내걸면서 성취를 이루지 못하고 낭비하게 되면 결국에는 사람들로부터 신뢰를 잃고 누구도 당신을 찾지 않게 될 수도 있음을 명심하기 바랍니다."
        elif h_center == 5 and metadata['ct'][5]==1:
            h_type = "방향 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = "방향센터 정의의 가장 큰 딜레마는 첫째로 “모든 사람들이 다들 자신이 어디를 향하여 가고 있는지 알고 있을 것이다” 라고 너무나 당연하게 생각한다는 점과, 둘째로 “내가 느끼는(자신이 향하는) 이 방향이 옳은 길이다” 라고 지나치게 다른 사람들에게 밀어붙일 수 있다는 점입니다."
            msg2 = "모두의 길이 똑같지 않고 각자의 길이 다르다는 점을 이해하지 못한 채 사람들에게 지시하고 방향을 가르쳐주겠다며 이끌려고 할 경우 오히려 분열을 야기하고 불협화음을 만들 수 있습니다. 방향센터는 마치 자석처럼 작동하는데 양극을 모두 가지지 않고 한쪽 극만 가지고 있어 끌어당김만이 작용합니다."
            msg3 = "바로 사랑이죠. 우리는 사랑을 서로 주고 받는 다라고 생각하지만, 실제로 더 정확히는 어느 한쪽이 반드시 더 주도적으로 사랑하게끔 되어있다는 것입니다. 특히 주로 방향센터 정의가 사랑을 하는 쪽(주는 쪽)이 되고, 방향센터가 미정인 사람은 그것이 자신의 마음에 들 경우 증폭/반영해주게 되는 것이죠."
        elif h_center == 6 and metadata['ct'][6]==1:
            h_type = "표현 센터 ( 정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = "당신의 표현센터가 생각센터와 연결되면 자신이 정리한 논리와 개념들, 주장들을 내세우게 됩니다. 만약 직관센터와 연결되어 있다면 순간순간의 직감, 특히나 생존이나 안전, 건강에 대한 것들에 대해 표현하려고 합니다. 방향센터와 연결되어 있다면 자신의 정체성, 혹은 나아가야 하는 방향에 대해, 사랑에 대해 표현하려 하고, 활력센터와 연결되어 있다면 자신의 활력반응을 그대로 표현하고 실행하게 됩니다."
            msg2 = "에고센터와 연결되어 있다면 자신의 의지/약속을 “나는 이걸 하고 싶어, 저걸 가지고 싶어, 이렇게 이렇게 하겠어” 와 같은 방식으로 드러내게 되고, 감정센터와 연결되어 있다면 나의 감정상태, 기분에 따라 행동하고 이야기합니다"
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
            msg = "외부로부터 압박감을 느낄 때는 두가지 방법으로 대처할 수 있습니다. 한가지는 그 압박감에 휘둘리지 않고 잠시 자신만의 공간으로 물러나 심호흡 하며 정돈하는 것이고, 다른 하나는 그 압박감에 기꺼이 자신을 내맡겨 상황 자체를 자신에게 유리하게 사용하는 것입니다."
            msg2 = "대부분의 경우에는 그저 뭔 지 모를 압박감과 불편함에 무엇이라도 하면서 자신을 바쁘게 만들 뿐, 그것이 좋은 성과나 어떤 결과물로 이어지지는 못합니다. 오히려 좌충우돌 사고만 치고 사건만 만들기 쉽죠. 당신은 그러한 압박으로부터 자유로울 수 있는 존재라는 것을 잊지 말기 바랍니다."
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
            msg = "직관센터가 미정인 사람들은 가까운 사람들이 발신하는 에너지에 영향을 받아 안정감을 느끼는 경우가 많습니다. 그것이 그 사람에 대한 의존성을 크게 만들기도 합니다. 특히 가족관계나 연인관계에서 더욱 그렇습니다. 그 사람의 존재(영향력)가 나의 생존을 보장해주는 느낌이니까요. 이렇게 직관센터가 정의되어 있는 사람의 영향력에 얽메여 있게 된 경우,  그 사람이 주는 직관 정의의 안정감이 너무 크기 때문에 언제 헤어져야 할지, 제대로 관계를 정리해야 할지 모를 수 있습니다."
        elif h_center == 3 and metadata['ct'][3]==0:
            h_type = "감정 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = "당신의 감정센터는 마치 열려 있는 창문과 같습니다. 여러 감정들을 받아들이고 그것을 분석합니다. 여기서 잊지 말아야 할 점은 객관성을 잃어서는 안된다는 점입니다. 그 감정에 빠져들거나 개인적인 것으로 받아들여선 안됩니다. 그렇게 되면 창문은 투명성을 잃고, 전체의 감정이 아닌 자신이 원하는 편협적이고 일부분의 감정들만 받아들이고, 나머지는 외면하거나 거절하게 됩니다."
            msg2 = "그렇게 점차 자신의 감정상태 뿐만 아니라 주변의 감정 상태에 대해서도 혼란스러움만 커지고 감정 업 다운에 끊임없이 휩쓸릴 경우, 그 불편함을 해소하기 위해 오히려 더욱 과민하게 반응하거나, 별 일 아닌 데도 과장되게 더 억지스럽게 표현하곤 합니다. 다른 사람들의 감정에 좌우되지 않도록 주의하기 바랍니다."
        elif h_center == 4 and metadata['ct'][4]==0:
            h_type = "에고 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = "하지만, 에고센터가 정의되어 있는 사람들과 섞여 살수 밖에 없으므로 그들이 발신하는 에너지를 수신하고 심지어 증폭함으로써 쓸데없는 약속을 하거나 자신을 채찍질하고 밀어붙이는 삶을 살게 되기 쉽습니다. 우리가 살아가는 현대사회에서는 항상 “우리는 더 빠르고, 예쁘고, 강하고, 성공적이고, 부자일 수 있다!” 라는 에너지로 가득합니다. 에고센터 미정인 당신은 이 에너지 안에 갇혀 함정에 빠진 채 끊임없이 자신을 채찍질하고 밀어붙입니다. 자신이 내건 약속을 지키기 위해 이들은 더 큰 약속을 만들기를 반복하고, 결국 자신의 무능력을 느끼며 다시 추락합니다. 실패할 때 마다, 더 상황은 나빠지고 자존감은 바닥에 떨어지게 되죠."
            msg2 = "당신이 지금 약속을 지키기 위한 큰 부담을 갖고 있거나, 자신의 무능력에 대한 자괴감에 시달리고 있다면, 그러한 부담감이 어디서부터 출발하고 있는지 돌아보면 좋겠습니다. 당신은 그러한 것으로부터 자유로운 사람으로 디자인되었음을 다시한번 돌아보시기 바랍니다."
        elif h_center == 5 and metadata['ct'][5]==0:
            h_type = "방향 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = "당신은 특히 장소에 민감합니다. 당신에게 알맞은 장소가 아니라면 그곳에서 만나는 사람들 또한 적합하지 않을 확률이 매우 높습니다. 좋은 사람을 만나고 싶다면 당신에게 좋은 느낌을 주는 장소들을 찾아야 합니다. 아무리 좋은 사람을 만나더라도 장소가 마음에 들지 않는다면 그 사람과 어떠한 흐름도 이어지지 않습니다. 새로운 장소에서 다시 시작해 보세요. 이것이 바로 당신이 자신의 방향을 찾아가는 방법입니다."
            msg2 = "아무리 좋은 사람을 만나더라도 장소가 마음에 들지 않는다면 그 사람과 어떠한 흐름도 이어지지 않습니다. 새로운 장소에서 다시 시작해 보세요. 이것이 바로 당신이 자신의 방향을 찾아가는 방법입니다."
            #msg3 = "그래서 ‘나는 누구인가?’라는 의문에 대한 답을 찾아 이리저리 돌아다니기도 합니다. 하지만 이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향 조건화입니다. 이로 인해 당신은 위와 같은 현상을 겪을 수 있지만. 이는 문제가 아닙니다. "
            #msg4 = "당신은 다양한 사람들의 사랑, 방향, 정체성을 경험하는 것을 통해 지혜로워질 잠재성이 있습니다. 전체 인류의 약 43%는 이 센터가 정의되어 있지 않습니다."
        elif h_center == 6 and metadata['ct'][6]==0:
            h_type = "표현 센터 ( 미정의 )"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = "당신은 다른 사람들의 주의를 끌기 위해 노력하기도 합니다. 다른 사람들이 당신에게 관심을 가져주지 않을까 걱정하고 주의를 끌기 위해 노력하는 경우가 있을 수 있습니다. 이것은 진정한 모습을 잃어버린 경우입니다. 쓸데없는 말을 많이 하게 되고, 어수선하고 번잡스러운 행동을 하거나, 인상을 남기기 위해 억지 모습을 보이는 것 등이 해당됩니다."
            #msg2 = "말과 행동의 방식이 일관되지 않은 당신은 말이나 행동을 할 때 불안감에 휩싸이기도 합니다. ‘무슨 말이든 해야할 것 같은데? 무슨 말을 해야하지? 가만히 있어도 되나?’ 라는 생각을 하며 말과 행동에 대한 압박을 느끼기 때문에 계속 말하고, 지나치게 말하고, 아무 말이나 하는 것입니다. "
            #msg3 = "이것은 자신으로부터 비롯된 것이 아닌, 외부의 영향입니다. 이로 인해 당신은 위와 같은 현상을 겪을 수 있고, 다른 사람들과의 소통에 있어서 힘들어질 수 있기 때문에 지나친 말과 행동에 유의해야 합니다. 당신이 먼저 말을 시작하기 보다는 가능한 다른 사람들이 당신에게 말을 걸었을 때, 얘기를 시작하는 것이 좋습니다."
            #msg4 = "당신은 다양한 방식으로 표현을 할 수 있으며, 누구의 말이 더 신뢰할 수 있는지를 잘 구별할 수 있는 잠재성이 있습니다.전체 인류의 약 28%는 이 센터가 정의되어 있지 않습니다."
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
                FollowupAction(name="action_question_intro")]

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

        return [SlotSet('bot_question', unego_question[1]), SlotSet("is_question", 0),
                SlotSet("center_type", center_type), SlotSet("center_step", center_step),
                SlotSet("center_question", True), SlotSet("step", step), SlotSet("is_sentiment", True)]

class ActionCenterDetailIntro(Action):
    def name(self) -> Text:
        return "action_center_detail_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_center_detail_intro')
        # 자세히 설명하기 위한 인트로 (센터별로 다르기때문에 새로 구현)
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "se": [2, 0, 6], "t": 3, "p": 52}

        center_step = tracker.get_slot("center_step")
        center_priority = tracker.get_slot('center_priority')
        h_center = center_priority[center_step]

        buttons = []
        buttons.append({"title": f'네. 듣고 싶어요', "payload": "/leading_centers"})
        buttons.append({"title": f'아뇨 괜찮아요', "payload": "/question_intro"})

        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            dispatcher.utter_message("다른 두개의 센터와의 관계도 설명해 볼까요?", buttons=buttons)
        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            dispatcher.utter_message("더 자세히 듣고 싶으신가요?", buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            dispatcher.utter_message("직관센터는 당신의 건강과 밀접합니다. 좀더 설명을 들으시겠어요?", buttons=buttons)

        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            dispatcher.utter_message("감정의 사이클이라는 것이 좀 어색하죠? 조금더 설명을 들어보시겠어요?", buttons=buttons)

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            dispatcher.utter_message("자, 에고센터 정의인 사람들에 대해 좀더 설명해볼까요?", buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            dispatcher.utter_message("자, 당신의 방향센터에 대해 이해가 되셨나요? 당신이 갖게 되는 딜레마에 대해서도 설명해 볼까요?", buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            dispatcher.utter_message("어떤 상황들이 있을 수 있는지 좀더 얘기해 볼까요?", buttons=buttons)
        elif h_center == 7 and metadata["ct"][7] == 1:
            h_type = "생각 센터 ( 정의 )"
            dispatcher.utter_message("더 자세히 듣고 싶으신가요?", buttons=buttons)
        elif h_center == 8 and metadata["ct"][8] == 1:
            h_type = "영감 센터 ( 정의 )"
            dispatcher.utter_message("더 자세히 듣고 싶으신가요?", buttons=buttons)


        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            dispatcher.utter_message("자, 이제는 극복할 수 있는 방법에 대해 좀더 얘기해볼까요?", buttons=buttons)
        elif h_center == 1 and metadata['ct'][1] == 0:
            h_type = "활력 센터 ( 미정의 )"
            dispatcher.utter_message("더 자세히 듣고 싶으신가요?", buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            dispatcher.utter_message("자, 당신이 알아야 할 점을 좀더 얘기해 볼까요?", buttons=buttons)
        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            dispatcher.utter_message("자, 감정센터와 관련되어 조심할 점을 좀더 얘기해 볼까요?", buttons=buttons)
        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            dispatcher.utter_message("자, 에고센터 미정인 사람들이 빠지기 쉬운 함정에 대해 좀더 설명해줄까요?", buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            dispatcher.utter_message("자, 당신의 정체성과 방향성에 대해 이해가 되셨나요? 당신에 대해 흥미로운 조언을 좀더 해드릴까요?", buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            dispatcher.utter_message("당신의 좋은 모습을 이해할 수 있겠죠? 좋지 않은 모습에 대해서도 알려줄까요?", buttons=buttons)
        elif h_center == 7 and metadata['ct'][7] == 0:
            h_type = "생각 센터 ( 미정의 )"
            dispatcher.utter_message("더 자세히 듣고 싶으신가요?", buttons=buttons)
        elif h_center == 8 and metadata['ct'][8] == 0:
            h_type = "영감 센터 ( 미정의 )"
            dispatcher.utter_message("더 자세히 듣고 싶으신가요?", buttons=buttons)

        return []
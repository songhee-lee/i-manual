import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker
from rasa_sdk.events import FollowupAction
import time

logger = logging.getLogger(__name__)

import pandas as pd
type_description_csv = pd.read_csv("./data/type_description.csv")
type_description = []
for i in range(0, 60):
    type_description.append(type_description_csv.iloc[i,1])

class ActionLeadingTypeIntro(Action):
    def name(self) -> Text:
        return "action_leading_type_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type_intro')

        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        is_finished = tracker.get_slot('is_finished')

        if leading_priority is None or step is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]

        if is_finished == 1:
            dispatcher.utter_message(
                type_description[0]
            )

        if (metadata["t"] == 0):
            # 에너자이저
            dispatcher.utter_message(
                type_description[1])
        elif (metadata["t"] == 1):
            # 스피드 에너자이저
            dispatcher.utter_message(
                type_description[2])
        elif (metadata["t"] == 2):
            # 혁신주도가
            dispatcher.utter_message(
                type_description[3])
        elif (metadata["t"] == 3):
            # 가이드
            dispatcher.utter_message(
                type_description[4])
        elif (metadata["t"] == 4):
            # 거울
            dispatcher.utter_message(
                type_description[5])

        h_type = ''
        msg_1 = ""
        msg_2 = ""
        msg_3 = ""
        msg_4 = ""
        msg_5 = ""
        if metadata["t"] == 0:
            h_type = "에너자이저 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_0.png"
            msg_1 = type_description[6]
            msg_2 = type_description[7]
            msg_3 = type_description[8]
        elif metadata["t"] == 1:
            h_type = "스피드 에너자이저 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_1.png"
            msg_1 = "당신은 자신이 사랑하는 것이나 관심있는 일에 에너지를 사용하는 사람들입니다. 더욱이 당신은 그 에너지를 빠르게 실천으로 옮기는 행동력도 지니고 있습니다. 이러한 사람들을 스피드에너자이저 종족, 또는 매니페스팅 제너레이터(Manifesting Generator) 종족이라고 부릅니다. 이 세상은 당신과 같은 종족의 사람들이 건설하는 곳입니다."
            msg_2 = "당신은 꾸준히 단계를 밟아가기 보다는 몇단계씩 건너뛰기도 하고, 때론 다시 돌아와 놓친 부분을 해내기도 합니다. 잠시도 가만히 있지 않고, 계속해서 뭔가를 하는 당신은 빠릿빠릿하다는 얘기를 자주 듣는 편입니다. 여러가지 일들을 빠르게 진행하다보니 빠트리거나 놓치기도 합니다. "
            msg_3 = "당신은 빠르게 결과를 보여주려고 하지만 조급하지 않게 여유를 갖고 일처리를 할 수 있도록 노력하는 것이 좋습니다. 또한, 자신을 돌볼 시간을 갖는 것도 잊지 말기 바랍니다."
        elif metadata["t"] == 2:
            h_type = "혁신주도가 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_2.png"
            msg_1 = "당신은 자신도 모르게 다른 사람들에게 차가운 에너지를 발신하는데, 그 이유는 자신이 하고 싶은 일에만 집중하고 다른 사람들에 대해서는 큰 관심이 없기 때문입니다. 이러한 사람들을 혁신주도가 종족 또는 메니페스터(Manifester) 종족이라고 부릅니다. "
            msg_2 = '옛날에 태어났다면 왕이나 제사장을 했을 종족입니다. 혁신을 주도하고 새로운 일들이 시작될 수 있도록 현시하는 것에 집중합니다. '
            msg_3 = "즉, 당신이 원하는 것을 즉시 표현하고 드러내고 실행하고 실체화시킬 수 있는 에너지를 가졌다는 것입니다. 다만, 어떻게 하면 사람들과 더 조화롭게 지낼 수 있을지에 대해서는 약간 어려움을 느낄 수도 있고, 자주 크고 작은 마찰을 겪었을지도 모르겠네요."
        elif metadata["t"] == 3:
            h_type = "가이드 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_3M.png"
            msg_1 = "당신과 같은 능력을 가진 사람들을 가이드 종족 또는 프로젝터(Projector) 종족이라고 부릅니다. 즉, 다른 사람들의 마음을 읽고 그들을 잘 가이드 할 수 있다는 의미에서의 가이드입니다. 또는 다른 사람의 속마음을 투사할 수 있는 능력이 있다는 점에서 프로젝터라고 불리기도 합니다. "
            msg_2 = '다만 가이드 종족은 언제나 그 길이 보이지만, 상대방의 입장에서는 내가 원하지도 않았는데 나를 꿰뚫어보는 느낌이 달갑지 않을 수 있기 때문에, 초대가 없이 먼저 나서서 달려들면 환영받지 못하거나, 기껏 다 도와주고서도 보상이나 좋은 말을 듣기는커녕 시기나 질투, 비아냥거림의 희생자가 될 수도 있습니다. '

        elif metadata["t"] == 4:
            h_type = "거울 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png"
            msg_1 = "당신은 이제까지 살아오면서 특이하다는 말도 많이 들었을 테고, 하고 싶은 게 도대체 뭐니? 라는 말도 정말 많이 들었을 거예요. 당신은 거울과 같은 존재입니다. "
            msg_2 = "당신은 다른 사람들의 에너지를 반사하는 능력을 갖고 있습니다. 그래서 당신과 같은 사람들을 거울 종족, 또는 리플렉터(Reflector) 종족이라고 부릅니다. 당신은 무한한 지혜의 잠재력을 가지고 있습니다. "
            msg_3 = "하지만 그 특별함 만큼이나 세상을 살아가는 현실적인 부분에 있어서는 어려움이 따를 수도 있지요. 자기 자신도 몰랐을 수 있는 진정한 당신의 모습을 한 번 알아볼까요? "
            msg_4 = "거울종족은 유별납니다. 자기만의 고유한 에너지가 단 하나도 없는 거울 종족은 자신의 주변 사람들, 자신의 주변 환경을 있는 그대로 흡수하여 보여주게 됩니다. "
            msg_5 = "거울 종족이 머무는 곳이 건강하다면, 함께하는 주변인들이 건강하다면 거울 종족도 생기가 넘치게 되고, 그렇지 못할 경우 거울 종족은 점차 피폐해지게 됩니다. 폐인이 됩니다. "

        # 인트로 다음 이미지
        dispatcher.utter_message(image=img)

        dispatcher.utter_message(msg_1)
        dispatcher.utter_message(msg_2)
        if msg_3 != "":
            dispatcher.utter_message(msg_3)
        if msg_4 != "":
            dispatcher.utter_message(msg_4)
        if msg_5 != "":
            dispatcher.utter_message(msg_5)

        if leading_priority[0]==0:
            step = 1
        elif leading_priority[1]==0:
            step = 2
        elif leading_priority[2]==0:
            step = 3
        elif leading_priority[3]==0:
            step = 4

        buttons = []
        buttons.append({"title": f'예', "payload": "/leading_type"})
        buttons.append({"title": f'아니요', "payload": "/leading_type_question"})
        if metadata["t"] == 2 or metadata["t"] == 3 or metadata["t"] == 4:
            dispatcher.utter_message(f'어때요? 중요한 얘기들이 아직 남아 있는데, 당신의 종족에 대해 좀더 알아볼까요?', buttons=buttons)
            return [SlotSet('step', step)]
        else:
            dispatcher.utter_message(f'자, {h_type}에 대해 이해가 되셨나요?')
            return [SlotSet('step', step), FollowupAction(name='action_leading_type_question')]



class ActionLeadingType(Action):
    def name(self) -> Text:
        return "action_leading_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type')

        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot('leading_priority')
        if leading_priority is None:
            return [FollowupAction(name='action_set_priority_again')]

        h_type = ''
        msg_1 = ""
        msg_2 = ""
        msg_3 = ""
        msg_4 = ""
        msg_5 = ""
        if metadata["t"] == 2:
            h_type = "혁신주도가 종족"
            msg_1 = "수직적 계급사회를 이루던 때에는 주로 고위층이었기에 자신들의 영향력을 발휘하는 것에 저항이나 어려움이 비교적 적었겠지만, 현대사회에서는 모두가 평등하고 자유로운 시대이다 보니, 당신의 종족들은 때때로 사람들로부터 저항을 받거나, 다른 이들이 당신의 행동에 대해 불편하게 느끼는 경우가 종종 있습니다. 마찰을 겪게 되는거죠. "
            msg_2 = '당신은 지극히 독립적이며, 자신이 하고자 하는 일에 방해받고 싶어하지 않습니다. 그렇게 하기 위해서는 꼭 알아야 하는 삶의 전략이 바로 알려주기입니다. '
            msg_3 = '내가 뭔가를 하고자 할 때, 혹은 뭔가를 이미 하고 있는 와중이더라도, 나의 주변인에게 미리 내가 무엇을 할 것인지 혹은 지금 내가 무엇을 하고 있는지 알려주기를 통해서 그들과의 마찰을 최소화할 수 있습니다. '
            msg_4 = "독립심이 강한 혁신주도가에게는 매번 이렇게 자신이 하는 일을 알리는 것 자체로도 너무나 번거롭고 귀찮은 도전일 수 있지만, 그를 통해 사람들은 당신의 행동에 충격을 받거나, 압도되거나, 불편함을 느끼지 않고 평화와 조화를 이룰 수 있습니다. "
        elif metadata["t"] == 3:
            h_type = "가이드 종족"
            msg_1 = "가이드 종족인 여러분에게 가장 중요한 것은 다른 사람으로부터 인정받고 초대받는 것입니다. 심지어는 초대가 오더라도 한두번 거절하면서 심사숙고하여 결정해야합니다. "
            msg_2 = '한번 초대를 받아들이면 그 일에 에너지가 묶여 스스로 쉽게 빠져나오지 못하거나, 더 좋은 기회가 오더라도 놓치게 될 수 있습니다. '
            msg_3 = "가이드 종족은 자기자신의 모습이 아닌 삶을 살 경우 씁쓸함을 맛보게 됩니다. 그와 반대로 자신의 모습 그대로의 삶을 살 경우에는 성공가도를 달리게 되죠."
            msg_4 = "다른 이들이 가진 잠재력과 독창성을 알아보며 그들을 성공으로 안내하는 것이 바로 가이드 종족의 성공입니다."
            msg_5 = "가이드 종족의 꿰뚫는 안목으로 다른 이들에게 유레카!를 안겨주는 질문을 한다던지 그들이 미처 모르고 지나친 부분에 대해 깨달음을 얻을 수 있게 돕습니다."
        elif metadata["t"] == 4:
            h_type = "거울 종족"
            msg_1 = "거울종족은 그야말로 자신이 머무는 환경을 그대로 흡수/반영합니다. 당신이 머무는 장소, 곁에 있는 사람들이 바로 당신의 삶을 결정하는 것이지요."
            msg_2 = "거울종족은 그저 그 모든 좋은 것과 나쁜 것 전부가 다양성의 한 부분일 뿐이라는 것을 알려주기 위해 존재하는 사람들입니다. 그 모든 다양성을 경험하는 것은 그야말로 놀라움 그 자체이지요. "
            msg_3 = "만약 뭔가 새로운 결심을 해야겠다면, 나에게 주어진 선택지 중에서 골라야 하는 상황이라면, 반드시 약 한달간달의 흐름이 지나는 동안 많은 경험과 맛보기를 통해 무엇이 자신에게 가장 건강한 선택인지 명료함을 얻어야 합니다. "

        dispatcher.utter_message(msg_1)
        dispatcher.utter_message(msg_2)
        if msg_3 != "":
            dispatcher.utter_message(msg_3)
        if msg_4 != "":
            dispatcher.utter_message(msg_4)
        if msg_5 != "":
            dispatcher.utter_message(msg_5)

        dispatcher.utter_message(f'자, {h_type}에 대해 이해가 되셨나요?')

        if leading_priority[0]==0:
            return [SlotSet('step', 1), FollowupAction(name='action_leading_type_question')]
        elif leading_priority[1]==0:
            return [SlotSet('step', 2), FollowupAction(name='action_leading_type_question')]
        elif leading_priority[2]==0:
            return [SlotSet('step', 3), FollowupAction(name='action_leading_type_question')]
        elif leading_priority[3]==0:
            return [SlotSet('step', 4), FollowupAction(name='action_leading_type_question')]


class ActionLeadingTypeQuestion(Action):
    def name(self) -> Text:
        return "action_leading_type_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type_question')
        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot('leading_priority')

        buttons = []

        if metadata["t"] == 0:

            buttons.append({"title": f'어떤 에너지를 가지고 있나요?',
                            "payload": "/type_question{\"bot_question\":\"어떤 에너지를 가지고 있나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'힘들 때 어떻게 해야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"힘들 때 어떻게 해야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'에너자이저의 전략은 뭔가요?',
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저의 전략은 뭔가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'에너자이저 아이는 어떻게 키워야 하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 1:

            buttons.append({"title": f'어떤 단점이 있을까요?',
                            "payload": "/type_question{\"bot_question\":\"어떤 단점이 있을까요?\", \"context_index\": 0}"})
            buttons.append({"title": f'힘들 때 어떻게 해야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"힘들 때 어떻게 해야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'스피드 에너자이저의 전략은 뭔가요?',
                            "payload": "/strategy_question{\"bot_question\":\"스피드 에너자이저의 전략은 뭔가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'스피드 에너자이저 아이는 어떻게 키워야 하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 2:
            buttons.append({"title": f'어떻게 살아가야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"어떻게 살아가야 하나요?\", \"context_index\": 0}"})
            buttons.append({"title": f'주변 사람들은 왜 저를 힘들게 할까요?',
                            "payload": "/type_question{\"bot_question\":\"주변 사람들은 왜 저를 힘들게 할까요?\", \"context_index\": 0}"})
            buttons.append({"title": f'혁신주도가의 전략은 무엇인가요?',
                            "payload": "/strategy_question{\"bot_question\":\"혁신주도가의 전략은 무엇인가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'알림은 어떻게 해야하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"알림은 어떻게 해야하나요?\", \"context_index\": 0}"})
            buttons.append({"title": f'혁신주도가 아이는 어떻게 키워야 하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"혁신주도가 아이는 어떻게 키워야 하나요?\", \"context_index\": 1}"})
        elif metadata["t"] == 3:
            buttons.append({"title": f'어떻게 살아가야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"어떻게 살아가야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'어떤 장점이 있을까요?',
                            "payload": "/type_question{\"bot_question\":\"어떤 장점이 있을까요?\", \"context_index\": 1}"})
            buttons.append({"title": f'가이드 아이는 어떻게 키워야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"가이드 아이는 어떻게 키워야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'초대를 기다린다는게 무슨 뜻인가요?',
                            "payload": "/strategy_question{\"bot_question\":\"초대가 무엇인가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'초대를 받은 후 어떻게 해야하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"초대를 받은 후 어떻게 해야하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 4:

            buttons.append({"title": f'어떻게 살아가야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"어떻게 살아가야 하나요?\", \"context_index\": 0}"})
            buttons.append({"title": f'거울 종족의 전략은 무엇인가요?',
                            "payload": "/strategy_question{\"bot_question\":\"거울 종족의 전략은 무엇인가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'한 달간 기다리지 않으면 안되나요?',
                            "payload": "/strategy_question{\"bot_question\":\"한 달간 기다리지 않으면 안되나요?\", \"context_index\": 0}"})
            buttons.append({"title": f'잘 기다리려면 어떻게 해야되나요?',
                            "payload": "/strategy_question{\"bot_question\":\"거울 종족의 기다림을 어떻게 도와줘야 하나요?\", \"context_index\": 0}"})
            buttons.append({"title": f'거울 종족 아이는 어떻게 키워야 하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"거울 종족 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        buttons.append({"title": f'질문 없어요', "payload": "/leading_more"})
        dispatcher.utter_message(f'질문이 있다면 다음 중에서 선택해보세요', buttons=buttons)

        return []

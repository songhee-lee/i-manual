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

class ActionLeadingTypeIntro(Action):
    def name(self) -> Text:
        return "action_leading_type_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type_intro')

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "t": 3, "p": 52}
        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        is_finished = tracker.get_slot('is_finished')
        if is_finished == True:
            dispatcher.utter_message(
                f'그럼 종족에 대해 다시 알려드릴게요!'
            )
        else:
            if leading_priority[0]==0: #종족이 첫번째 설명이라면
                if (metadata["t"] == 0):
                    # 가이드
                    dispatcher.utter_message(
                        f'에너자이저 종족 인트로')
                elif (metadata["t"] == 1):
                    # 스피드 에너자이저
                    dispatcher.utter_message(
                        f'스피드 에너자이저 종족 인트로')
                elif (metadata["t"] == 2):
                    # 혁신주도가
                    dispatcher.utter_message(
                        f'안녕하세요, {metadata["pn"]}님은 인류의 10%에 해당하는 사람입니다.')
                elif (metadata["t"] == 3):
                    dispatcher.utter_message(
                        f'안녕하세요, {metadata["pn"]}님은 인류의 23%에 해당하는 사람입니다.')
                elif (metadata["t"] == 4):
                    # 거울
                    dispatcher.utter_message(
                        f'안녕하세요, {metadata["pn"]}님은 인류의 1%에 해당하는 정말 정말 특별한 사람입니다.')
            else:
                dispatcher.utter_message(
                    f'다음으로 종족을 살펴보겠습니다.')
        h_type = ''
        if metadata["t"] == 0:
            h_type = "에너자이저 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_0.png"
            msg_1 = "인류의 37%를 차지하는 꾸준함의 종족이에요. 이 시대에서 꼭 필요한 절대 지치지 않는 에너지를 가지고 있는 성실함의 아이콘!"
            msg_2 = "뿜뿜! 힘이 넘치는 에너자이저 종족은 잠들기 전에 자신이 가진 에너지를 모두 소진하고 잠드는게 다음 날 더 개운하고 만족스러운 수면을 취할 수 있답니다. 자신의 에너지를 완전히 몰두시킬만한 일이 뭔지 찾아보고, 그 일이 나에게 맞는지 '활력센터의 반응'을 통해 결정한다면 틀림 없이 만족을 경험할 수 있을 거에요 "
            msg_3 = ""
        elif metadata["t"] == 1:
            h_type = "스피드 에너자이저 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_1.png"
            msg_1 = "인류의 33%를 차지하는 민첩함의 종족이에요. 본능적으로 행동이 앞서는 실천력, 모든 일을 수용할 수 있는 융통성까지 갖춘 행동대장!"
            msg_2 = "힘이 넘치는 에너자이저에 빠른 스피드까지! 스피드 에너자이저는 너무 급하게 움직이다가 뭔가를 놓치고 빼먹거나 깜박 잊고 지나치는 경우가 있을 수 있어요. 중간점검을 하면서 잊어버리거나 못보고 지나친 부분은 없는지 살펴보는게 좋을 것 같아요. 아참! 스피드 에너자이저도 결국에는 에너자이저 종족 이므로 '활력센터 반응'을 꼭 따라야 한다는 점! 잊지마세요~ "
            msg_3 = ""
        elif metadata["t"] == 2:
            h_type = "혁신주도가 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_2.png"
            msg_1 = "이들은 자신도 모르게 다른 사람들에게 차가운 에너지를 발신하는데, 그 이유는 자신이 하고 싶은 일에만 집중하고 다른 사람들에 대해서는 큰 관심이 없기 때문입니다. 이러한 부류의 사람들을 혁신주도가 종족 또는 메니페스터(Menifester) 종족이라고 부릅니다. 옛날에 태어났다면 왕이나 제사장을 했을 종족입니다. 혁신을 주도하고 새로운 일들이 시작될 수 있도록 현시하는 것에 집중합니다."
            msg_2 = '즉, 당신이 원하는 것을 즉시 표현하고 드러내고 실행하고 실체화 시킬 수 있는 에너지를 가졌다는 것입니다. 다만, 어떻게 하면 사람들과 더 조화롭게 지낼 수 있을지에 대해서는 약간 어려움을 느낄 수도 있고, 자주 크고 작은 마찰을 겪었을지도 모르겠네요.'
            msg_3 = '수직적 계급사회를 이루던 때에는 주로 고위층이었기에 자신들의 영향력을 발휘하는 것에 저항이나 어려움이 비교적 별로 없었겠지만, 현대사회에서는 모두가 평등하고 자유로운 시대이다 보니, 당신의 종족들은 때때로 사람들로부터 저항을 받거나, 다른 이들이 당신의 행동에 대해 불편하게 느끼는 경우가 종종 있습니다. 마찰을 겪게 되는거죠.'
        elif metadata["t"] == 3:
            h_type = "가이드 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_3.png"
            msg_1 = "다른 사람들의 마음을 자기도 모르게 꿰뚫어 볼 수 있는 능력을 갖고 있습니다. 그래서, 우리는 이러한 사람들을 가이드 종족 또는 프로젝터(Projector) 종족이라고 부릅니다. 즉, 다른 사람들의 마음을 읽고 그들을 잘 가이드 할 수 있다는 의미에서의 가이드입니다. 또는 다른 사람의 속마음을 투사할 수 있는 능력이 있다는 점에서 프로젝터라고 불리기도 합니다."
            msg_2 = '다만 가이드 종족은 언제나 그 길이 보이지만, 상대방의 입장에서는 내가 원하지도 않았는데 나를 꿰뚫어보는 느낌이 달갑지 않을 수 있기 때문에, 초대가 없이 먼저 나서서 달려들면 바로 내쫓기거나, 기껏 다 도와주고서도 보상이나 좋은 말을 듣기는커녕 시기나 질투, 비아냥거림의 희생자가 될 수도 있습니다.'
            msg_3 = '따라서, 가이드 종족인 여러분에게 가장 중요한 것은 다른 사람으로부터 인정받고 초대받는 것입니다. 심지어는 초대가 오더라도 한두번 거절하면서 심사숙고하여 결정해야합니다. 한번 초대를 받아들이면 그 일에 에너지가 묶여 스스로 쉽게 빠져나오지 못하거나, 더 좋은 기회가 오더라도 놓치게 될 수 있습니다. 너무 장기적인 일, 평생을 바쳐야 하는 그런 일보다는 짧은 기간을 주기로 서로 계약을 갱신하거나 주기적으로 서로의 입장을 나눠볼 수 있는 비교적 자유로운 프로젝트 팀에 소속되는 것이 더 편안하고 자신에게 유리할 수 있습니다.'
        elif metadata["t"] == 4:
            h_type = "거울 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png"
            msg_1 = "이제까지 살아오면서 특이하다는 말도 많이 들었을 테고, 하고 싶은 게 도대체 뭐니? 라는 말도 정말 많이 들었을 거예요. 당신은 거울과 같은 존재입니다. 다른 사람들의 에너지를 반사하는 능력을 갖고 있습니다. 그래서 당신과 같은 사람들을 거울 종족, 또는 리플렉터(Reflector) 종족이라고 부릅니다."
            msg_2 = "당신은 무한한 지혜의 잠재력을 가지고 있습니다. 하지만 그 특별함 만큼이나 세상을 살아가는 현실적인 부분에 있어서는 어려움이 따를 수도 있지요. 자기 자신도 몰랐을 수 있는 진정한 당신의 모습을 한 번 알아볼까요?"
            msg_3 = "거울종족은 유별납니다. 자기만의 고유한 에너지가 단 하나도 없는 거울 종족은 자신의 주변 사람들, 자신의 주변 환경을 있는 그대로 흡수하여 보여주게 됩니다. 거울 종족이 머무는 곳이 건강하다면, 함께하는 주변인들이 건강하다면 거울 종족도 생기가 넘치게 되고, 그렇지 못할 경우 거울 종족은 점차 피폐해지게 됩니다. 폐인이 됩니다."


        dispatcher.utter_message(
             f'{metadata["pn"]}님, 당신은 {h_type}이시네요!', image=img)

        dispatcher.utter_message(msg_1)
        dispatcher.utter_message(msg_2)
        dispatcher.utter_message(msg_3)
        buttons = []
        buttons.append({"title": f'네. 더 알고싶어요', "payload": "/leading_type"})
        buttons.append({"title": f'아뇨 충분해요', "payload": "/question_intro"})
        dispatcher.utter_message(f'{h_type}에 대해 더 알고싶으신가요?', buttons=buttons)

        if leading_priority[0]==0:
            return [SlotSet('step', 1)]
        elif leading_priority[1]==0:
            return [SlotSet('step', 2)]
        elif leading_priority[2]==0:
            return [SlotSet('step', 3)]
        elif leading_priority[3]==0:
            return [SlotSet('step', 4)]

class ActionLeadingType(Action):
    def name(self) -> Text:
        return "action_leading_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type')

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "t": 3, "p": 52}
        leading_priority = tracker.get_slot('leading_priority')

        h_type = ''
        if metadata["t"] == 0:
            h_type = "에너자이저 종족"
            msg_1 = "인류의 37%를 차지하는 꾸준함의 종족이에요. 이 시대에서 꼭 필요한 절대 지치지 않는 에너지를 가지고 있는 성실함의 아이콘!"
            msg_2 = "뿜뿜! 힘이 넘치는 에너자이저 종족은 잠들기 전에 자신이 가진 에너지를 모두 소진하고 잠드는게 다음 날 더 개운하고 만족스러운 수면을 취할 수 있답니다. 자신의 에너지를 완전히 몰두시킬만한 일이 뭔지 찾아보고, 그 일이 나에게 맞는지 '활력센터의 반응'을 통해 결정한다면 틀림 없이 만족을 경험할 수 있을 거에요 "
        elif metadata["t"] == 1:
            h_type = "스피드 에너자이저 종족"
            msg_1 = "인류의 33%를 차지하는 민첩함의 종족이에요. 본능적으로 행동이 앞서는 실천력, 모든 일을 수용할 수 있는 융통성까지 갖춘 행동대장!"
            msg_2 = "힘이 넘치는 에너자이저에 빠른 스피드까지! 스피드 에너자이저는 너무 급하게 움직이다가 뭔가를 놓치고 빼먹거나 깜박 잊고 지나치는 경우가 있을 수 있어요. 중간점검을 하면서 잊어버리거나 못보고 지나친 부분은 없는지 살펴보는게 좋을 것 같아요. 아참! 스피드 에너자이저도 결국에는 에너자이저 종족 이므로 '활력센터 반응'을 꼭 따라야 한다는 점! 잊지마세요~ "
        elif metadata["t"] == 2:
            h_type = "혁신주도가 종족"
            msg_1 = "당신은 지극히 독립적이며, 자신이 하고자 하는 일에 방해받고 싶어하지 않습니다. 그렇게 하기 위해서는 꼭 알아야 하는 삶의 전략이 바로 알려주기입니다. 내가 뭔가를 하고자 할 때, 혹은 뭔가를 이미 하고 있는 와중이더라도, 나의 주변인에게, 특히 평소에도 나와 마찰을 겪던 사람이라면 더더욱, 미리 내가 무엇을 할 것인지 혹은 지금 내가 무엇을 하고 있는지 알려주기를 통해서 그들과의 마찰을 최소화할 수 있습니다."
            msg_2 = '독립심이 강한 혁신주도가에게는 매번 이렇게 자신이 하는 일을 알리는 것 자체로도 너무나 번거롭고 귀찮은 도전일 수 있지만, 그를 통해 사람들은 당신의 행동에 충격을 받거나, 압도되거나, 불편함을 느끼지 않고 평화와 조화를 이룰 수 있습니다.'
        elif metadata["t"] == 3:
            h_type = "가이드 종족"
            msg_1 = "가이드 종족은 자기자신의 모습이 아닌 삶을 살 경우 씁쓸함을 맛보게 됩니다. 그와 반대로 자신의 모습 그대로의 삶을 살 경우에는 성공가도를 달리게 되죠. 다른 이들이 가진 잠재력과 독창성을 알아보며 그들을 성공으로 안내하는 것이 바로 가이드 종족의 성공입니다."
            msg_2 = '가이드 종족의 꿰뚫는 안목으로 다른이들에게 유레카!를 안겨주는 질문을 한다던지 그들이 미처 모르고 지나친 부분에 대해 깨달음을 얻을 수 있게 돕습니다.'
        elif metadata["t"] == 4:
            h_type = "거울 종족"
            msg_1 = "거울종족은 그야말로 자신이 머무는 환경을 그대로 흡수/반영합니다. 당신이 머무는 장소, 곁에 있는 사람들이 바로 당신의 삶을 결정하는 것이지요. 거울종족은 그저 그 모든 좋은 것과 그 모든 나쁜 것 전부가 다양성의 한 부분일 뿐이라는 것을 알려주기 위해 존재하는 사람들입니다. 그 모든 다양성을 경험하는 것은 그야말로 놀라움 그 자체이지요."
            msg_2 = "만약 뭔가 새로운 결심을 해야겠다면, 나에게 주어진 선택지 중에서 골라야 하는 상황이라면, 반드시 약 한달간달의 흐름이 지나는 동안 많은 경험과 맛보기를 통해 무엇이 자신에게 가장 건강한 선택인지 명료함을 얻어야 합니다. 그렇지 않을 경우 실망감만 가득한 세상에 남게 될테니까요."

        dispatcher.utter_message(msg_1)
        dispatcher.utter_message(msg_2)
        buttons = []
        buttons.append({"title": f'네. 질문 있어요', "payload": "/leading_type_question"})
        buttons.append({"title": f'아뇨 질문 없어요', "payload": "/leading_more"})

        dispatcher.utter_message(f'자, {h_type}에 대해 이해가 되셨나요? {h_type}에 대한 질문이 있으신가요?', buttons=buttons)

        if leading_priority[0]==0:
            return [SlotSet('step', 1)]
        elif leading_priority[1]==0:
            return [SlotSet('step', 2)]
        elif leading_priority[2]==0:
            return [SlotSet('step', 3)]
        elif leading_priority[3]==0:
            return [SlotSet('step', 4)]


class ActionLeadingTypeQuestion(Action):
    def name(self) -> Text:
        return "action_leading_type_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type_question')
        # metadata = extract_metadata_from_tracker(tracker)
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "t": 3, "p": 52}
        leading_priority = tracker.get_slot('leading_priority')

        buttons = []
        if metadata["t"] == 0:

            buttons.append({"title": f'어떤 에너지를 가지고 있나요?',
                            "payload": "/type_question{\"bot_question\":\"어떤 에너지를 가지고 있나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'힘들 때 어떻게 해야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"힘들 때 어떻게 해야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'에너자이저의 전략은 뭔가요?',
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저의 전략은 뭔가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'어떤 질문을 해야 되나요?',
                            "payload": "/strategy_question{\"bot_question\":\"어떤 질문을 해야 되나요?\", \"context_index\": 0}"})
            buttons.append({"title": f'에너자이저 아이는 어떻게 키워야 하나요?',
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 1:

            buttons.append({"title": f'어떤 단점이 있을까요?',
                            "payload": "/type_question{\"bot_question\":\"어떤 단점이 있을까요?\", \"context_index\": 0}"})
            buttons.append({"title": f'힘들 때 어떻게 해야 하나요?',
                            "payload": "/type_question{\"bot_question\":\"힘들 때 어떻게 해야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": f'스피드 에너자이저의 전략은 뭔가요?',
                            "payload": "/strategy_question{\"bot_question\":\"스피드 에너자이저의 전략은 뭔가요?\", \"context_index\": 0}"})
            buttons.append({"title": f'어떤 질문을 해야 되나요?',
                            "payload": "/strategy_question{\"bot_question\":\"어떤 질문을 해야 되나요?\", \"context_index\": 0}"})
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

        dispatcher.utter_message(f'다음 질문중에서 선택해주세요', buttons=buttons)

        return []

#class ActionGetHumanDesignType(Action):
#    def name(self) -> Text:
#        return "action_get_humandesign_type"
#
#    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        entities = tracker.latest_message['entities']
#
#        metadata = extract_metadata_from_tracker(tracker)
#
#        for i in range(len(entities)):
#            h_type = (entities[i]['value'])
#
#        title = None
#        title = "거울 종족에 대해 설명할께요"
#        img = "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png"
#        msg_sub = "인류의 약 1%를 차지하는 카멜레온 종족이에요.주변의 분위기에 많은 영향을 받고, 많은 것을 받아들이며 투영하는 변화무쌍한 종족!"
#        msg = "중요한 선택의 기로에 선 당신! 당신이 만약 거울종족이라면, 한 달의 시간 동안 지속적으로 그 선택에 대해 고민하고 주변 사람들과 함께 이야기 나누며 정보를 모을 필요가 있어요. 만약 충분히 심사숙고 하지 않고 선택할 경우 높은 확률로 실망하게 될 수 있답니다. "
#        #if h_type == "reflector":
#        #    title = "거울 종족에 대해 설명할께요"
#        #    img = "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png"
#        #    msg_sub = "인류의 약 1%를 차지하는 카멜레온 종족이에요.주변의 분위기에 많은 영향을 받고, 많은 것을 받아들이며 투영하는 변화무쌍한 종족!"
#        #    msg = "중요한 선택의 기로에 선 당신! 당신이 만약 거울종족이라면, 한 달의 시간 동안 지속적으로 그 선택에 대해 고민하고 주변 사람들과 함께 이야기 나누며 정보를 모을 필요가 있어요. 만약 충분히 심사숙고 하지 않고 선택할 경우 높은 확률로 실망하게 될 수 있답니다. "
#        #elif h_type == "generator":
#        #    title = "에너자이저 종족에 대해 설명할께요"
#        #    img = "https://asset.i-manual.co.kr/static/images/share/profile/type_0.png"
#        #    msg_sub = "인류의 37%를 차지하는 꾸준함의 종족이에요. 이 시대에서 꼭 필요한 절대 지치지 않는 에너지를 가지고 있는 성실함의 아이콘!"
#        #    msg = "뿜뿜! 힘이 넘치는 에너자이저 종족은 잠들기 전에 자신이 가진 에너지를 모두 소진하고 잠드는게 다음 날 더 개운하고 만족스러운 수면을 취할 수 있답니다. 자신의 에너지를 완전히 몰두시킬만한 일이 뭔지 찾아보고, 그 일이 나에게 맞는지 '활력센터의 반응'을 통해 결정한다면 틀림 없이 만족을 경험할 수 있을 거에요 "
#        #elif h_type == "projector":
#        #    title = "가이드 종족에 대해 설명할께요"
#        #    img = "https://asset.i-manual.co.kr/static/images/share/profile/type_3.png"
#        #    msg_sub = "인류의 20%를 차지하는 인솔자 종족이에요. 날카로운 관찰력으로 세상을 꿰뚫어 보며 타인에게 관심이 많은 호기심 대장!"
#        #    msg = '"초대"라는 것의 범위가 우리의 생각보다 더 광범위 할 수 있답니다. 꼭 직접적으로 "너를 초대할게" 하는 초대가 아니더라도 간접적으로도 무수히 많은 초대가 주어지고 있기에 너무 걱정하지 않아도 될 것 같아요. 만약 뭔가 새롭게 하고 싶은게 생겼다면 그것을 내가 직접 진행하기 보다는 함께할만한 조력자와 이야기나눠 조력자를 통해 진행하면 더 좋을 것 같아요'
#        #elif h_type == "manifestor":
#        #    title = "혁신주도가 종족에 대해 설명할께요"
#        #    img = "https://asset.i-manual.co.kr/static/images/share/profile/type_2.png"
#        #    msg_sub = "인류의 9%를 차지하는 혁신 추구 종족이에요. 존재만으로도 사람들이 무언가를 실행에 옮기게끔 만드는 강한 에너지의 소유자!"
#        #    msg = '알림을 해줄 때에는 구체적이고 디테일하게 알려주는 것이 좋답니다. 무작정 "나 이거 할꺼야" 하는 통보나 일방적인 방식이 아니라 "내가 이런걸 하려고 하는데 어떻게 생각해?" 라는 약간은 열려있는 느낌으로 알림을 준다면, 상대방의 저항이나 반발을 겪지 않고 시작하게 될 확률이 높을거에요'
#        #elif h_type == "manifesting_generator":
#        #    title = "스피드 에너자이저 종족에 대해 설명할께요"
#        #    img = "https://asset.i-manual.co.kr/static/images/share/profile/type_1.png"
#        #    msg_sub = "인류의 33%를 차지하는 민첩함의 종족이에요. 본능적으로 행동이 앞서는 실천력, 모든 일을 수용할 수 있는 융통성까지 갖춘 행동대장!"
#        #    msg = "힘이 넘치는 에너자이저에 빠른 스피드까지! 스피드 에너자이저는 너무 급하게 움직이다가 뭔가를 놓치고 빼먹거나 깜박 잊고 지나치는 경우가 있을 수 있어요. 중간점검을 하면서 잊어버리거나 못보고 지나친 부분은 없는지 살펴보는게 좋을 것 같아요. 아참! 스피드 에너자이저도 결국에는 에너자이저 종족 이므로 '활력센터 반응'을 꼭 따라야 한다는 점! 잊지마세요~ "
#
#        if title is not None:
#            dispatcher.utter_message(title, image=img)
#            dispatcher.utter_message(msg_sub)
#            dispatcher.utter_message(msg)
#        else:
#            dispatcher.utter_message('찾고자 하는 종족을 저희가 찾지 못했어요. 다시 한번 확인하시어 입력해 주세요')
#            dispatcher.utter_message(json_message = {
#                "type": "tag", 'sender':metadata['uID'], "content": f'에너자이저 종족,스피드 에너자이저 종족,혁신주도가 종족,가이드 종족,거울 종족', "guide": f'검색 가능한 종족을 태그로 보여드릴게요.'})
#
#        buttons = []
#        buttons.append({"title": f'네. 이어서 사회적 성향에 대해 알아볼래요', "payload": "/leading_profile"})
#        buttons.append({"title": f'다른 종족도 알아보고 싶어요', "payload": "/type_common_mean"})
#        buttons.append({"title": f'이 항목 말고 다른 설명을 듣고 싶어요', "payload": "/leading_more"})
#
#        dispatcher.utter_message(
#             f'궁금하신 내용은 찾으셨나요?', buttons=buttons)
#        # dispatcher.utter_message("로케이션 세팅 완료!")
#        return []
#
#
#class ActionGetHumanDesignCommonType(Action):
#    def name(self) -> Text:
#        return "action_get_humandesign_common_type"
#
#    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        # {
#        #     "title": "Link name",
#        #     "url": "http://link.url",
#        #     "type": "web_url"
#        # },
#
#        metadata = extract_metadata_from_tracker(tracker)
#        print("MetaData: ", metadata)
#
#        dispatcher.utter_message(
#            "혈액형으로 사람을 구분하는 것처럼 인류는 크게 5가지의 종족으로 분류할 수 있어요. 인류의 9%는 시작하는 에너지를 갖는 혁신주도가 종족, 20%는 안내하는 에너지를 갖는 가이드 종족, 70%는 직접 해내고 이루는 에너지를 갖는 에너자이저 종족, 1%는 고정된 에너지가 없이 비추는 역할을 하는 거울 종족으로 나뉩니다.")
#
#        retVal = {
#            "type": "template",
#            "payload": {
#                "template_type": "generic",
#                "elements": [
#                    {
#                        "title": "에너자이저 종족",
#                        "subtitle": "반응하며 살면 좋아요",
#                        "image_url": "https://asset.i-manual.co.kr/static/images/share/profile/type_0.png",
#                        "buttons": [
#                            {
#                                "title": "자세히",
#                                "type": "postback",
#                                "payload": "에너자이저 종족이란 무엇인가요?"
#                            }
#                        ]
#                    },
#                    {
#                        "title": "스피드 에너자이저 종족",
#                        "subtitle": "반응하며 살면 좋아요",
#                        "image_url": "https://asset.i-manual.co.kr/static/images/share/profile/type_1.png",
#                        "buttons": [
#                            {
#                                "title": "자세히",
#                                "type": "postback",
#                                "payload": "스피드 에너자이저 종족이란 무엇인가요?"
#                            }
#                        ]
#                    },
#                    {
#                        "title": "혁신주도가 종족",
#                        "subtitle": "알리면서 살면 좋아요",
#                        "image_url": "https://asset.i-manual.co.kr/static/images/share/profile/type_2.png",
#                        "buttons": [
#                            {
#                                "title": "자세히",
#                                "type": "postback",
#                                "payload": "혁신주도가 종족이란 무엇인가요?"
#                            }
#                        ]
#                    },
#                    {
#                        "title": "가이드 종족",
#                        "subtitle": "초대를 기다려세요",
#                        "image_url": "https://asset.i-manual.co.kr/static/images/share/profile/type_3.png",
#                        "buttons": [
#                            {
#                                "title": "자세히",
#                                "type": "postback",
#                                "payload": "가이드 종족이란 무엇인가요?"
#                            }
#                        ]
#                    },
#                    {
#                        "title": "거울 종족",
#                        "subtitle": "28일동안 숙고하세요",
#                        "image_url": "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png",
#                        "buttons": [
#                            {
#                                "title": "자세히",
#                                "type": "postback",
#                                "payload": "거울 종족이란 무엇인가요?"
#                            }
#                        ]
#                    },
#                ]
#            }
#        }
#
#        dispatcher.utter_message(
#            text="각 종족에 대해 궁금하시면 아래 자세히 버튼을 눌러보세요", attachment=retVal)
#
#        print("get Step")
#        print(tracker.get_slot('step'))
#        print("get Step end")
#
#        buttons = []
#        buttons.append({"title": f'사회적 성향 알아보기', "payload": "/leading_profile"})
#        buttons.append({"title": f'이 항목 말고 다른 설명을 듣고 싶어요', "payload": "/leading_more"})
#
#        dispatcher.utter_message(
#             f'이어서 나의 사회적 성향을 알아보실래요?', buttons=buttons)
#
#        return []

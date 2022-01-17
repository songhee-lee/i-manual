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
            msg_1 = type_description[9]
            msg_2 = type_description[10]
            msg_3 = type_description[11]
        elif metadata["t"] == 2:
            h_type = "혁신주도가 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_2.png"
            msg_1 = type_description[12]
            msg_2 = type_description[13]
            msg_3 = type_description[14]
        elif metadata["t"] == 3:
            h_type = "가이드 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_3M.png"
            msg_1 = type_description[19]
            msg_2 = type_description[20]

        elif metadata["t"] == 4:
            h_type = "거울 종족"
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png"
            msg_1 = type_description[26]
            msg_2 = type_description[27]
            msg_3 = type_description[28]
            msg_4 = type_description[29]
            msg_5 = type_description[30]

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
            msg_1 = type_description[15]
            msg_2 = type_description[16]
            msg_3 = type_description[17]
            msg_4 = type_description[18]
        elif metadata["t"] == 3:
            h_type = "가이드 종족"
            msg_1 = type_description[21]
            msg_2 = type_description[22]
            msg_3 = type_description[23]
            msg_4 = type_description[24]
            msg_5 = type_description[25]
        elif metadata["t"] == 4:
            h_type = "거울 종족"
            msg_1 = type_description[31]
            msg_2 = type_description[32]
            msg_3 = type_description[33]

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

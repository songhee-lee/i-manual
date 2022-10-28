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
type_description.append(type_description_csv['korean'].values.tolist())
type_description.append(type_description_csv['english'].values.tolist())
type_description.append(type_description_csv['voiceID'].values.tolist())

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = []
etc_description.append(etc_description_csv['korean'].values.tolist())
etc_description.append(etc_description_csv['english'].values.tolist())
etc_description.append(etc_description_csv['voiceID'].values.tolist())

class ActionLeadingTypeIntro(Action):
    def name(self) -> Text:
        return "action_leading_type_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type_intro')

        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        is_finished = tracker.get_slot('is_finished')

        if leading_priority is None or step is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]

        if is_finished == 1:
            dispatcher.utter_message(
                type_description[lang][0]
            )

        if (metadata["t"] == 0):
            # 에너자이저
            dispatcher.utter_message(
                type_description[lang][1], json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/20201.wav"
            })
        elif (metadata["t"] == 1):
            # 스피드 에너자이저
            dispatcher.utter_message(
                type_description[lang][2])
        elif (metadata["t"] == 2):
            # 혁신주도가
            dispatcher.utter_message(
                type_description[lang][3])
        elif (metadata["t"] == 3):
            # 가이드
            dispatcher.utter_message(
                type_description[lang][4])
        elif (metadata["t"] == 4):
            # 거울
            dispatcher.utter_message(
                type_description[lang][5])

        h_type = ''
        msg_1 = ""
        msg_2 = ""
        msg_3 = ""
        msg_4 = ""
        msg_5 = ""
        if metadata["t"] == 0:
            h_type = type_description[lang][61] # 에너자이저 종족
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_0.png"
            msg_1 = type_description[lang][6]
            msg_2 = type_description[lang][7]
            msg_3 = type_description[lang][8]
            # 인트로 다음 이미지
            dispatcher.utter_message(image=img)

            dispatcher.utter_message(msg_1, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/20701.wav"
            })
            dispatcher.utter_message(msg_2, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/20801.wav"
            })
            dispatcher.utter_message(msg_3, json_message = {
                "type": "voiceID", 'sender':metadata['uID'], "content": "out_5/20901.wav"
            })

        elif metadata["t"] == 1:
            h_type = type_description[lang][62] # 스피드 에너자이저 종족
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_1.png"
            msg_1 = type_description[lang][9]
            msg_2 = type_description[lang][10]
            msg_3 = type_description[lang][11]
            # 인트로 다음 이미지
            dispatcher.utter_message(image=img)

            dispatcher.utter_message(msg_1)
            dispatcher.utter_message(msg_2)
            dispatcher.utter_message(msg_3)

        elif metadata["t"] == 2:
            h_type = type_description[lang][63] # 혁신주도가 종족
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_2.png"
            msg_1 = type_description[lang][12]
            msg_2 = type_description[lang][13]
            msg_3 = type_description[lang][14]
            # 인트로 다음 이미지
            dispatcher.utter_message(image=img)

            dispatcher.utter_message(msg_1)
            dispatcher.utter_message(msg_2)
            dispatcher.utter_message(msg_3)

        elif metadata["t"] == 3:
            h_type = type_description[lang][64] # 가이드 종족
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_3M.png"
            msg_1 = type_description[lang][19]
            msg_2 = type_description[lang][20]
            # 인트로 다음 이미지
            dispatcher.utter_message(image=img)

            dispatcher.utter_message(msg_1)
            dispatcher.utter_message(msg_2, json_message = {
                        "type": "voiceID", 'sender':metadata['uID'], "content": "out_긴문장/2.wav"
                    })

        elif metadata["t"] == 4:
            h_type = type_description[lang][65] # 거울 종족
            img = "https://asset.i-manual.co.kr/static/images/share/profile/type_4.png"
            msg_1 = type_description[lang][26]
            msg_2 = type_description[lang][27]
            msg_3 = type_description[lang][28]
            msg_4 = type_description[lang][29]
            msg_5 = type_description[lang][30]

            # 인트로 다음 이미지
            dispatcher.utter_message(image=img)

            dispatcher.utter_message(msg_1)
            dispatcher.utter_message(msg_2)
            dispatcher.utter_message(msg_3)
            dispatcher.utter_message(msg_4)
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
        buttons.append({"title": etc_description[lang][23], "payload": "/leading_type"}) # 예
        buttons.append({"title": etc_description[lang][24], "payload": "/leading_type_question"}) #아니오
        if metadata["t"] == 2 or metadata["t"] == 3 or metadata["t"] == 4:
            dispatcher.utter_message(type_description[lang][34], buttons=buttons)
            return [SlotSet('step', step)]
        else:
            message = type_description[lang][35].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/20903.wav"
            })
            return [SlotSet('step', step), FollowupAction(name='action_leading_type_question')]



class ActionLeadingType(Action):
    def name(self) -> Text:
        return "action_leading_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_type')

        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']

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
            h_type = type_description[lang][63] # 혁신주도가 종족
            msg_1 = type_description[lang][15]
            msg_2 = type_description[lang][16]
            msg_3 = type_description[lang][17]
            msg_4 = type_description[lang][18]
            dispatcher.utter_message(msg_1, json_message = {
                        "type": "voiceID", 'sender':metadata['uID'], "content": "out_긴문장/1.wav"
                    })
            dispatcher.utter_message(msg_2)
            dispatcher.utter_message(msg_3)
            dispatcher.utter_message(msg_4)
        elif metadata["t"] == 3:
            h_type = type_description[lang][64] # 가이드 종족
            msg_1 = type_description[lang][21]
            msg_2 = type_description[lang][22]
            msg_3 = type_description[lang][23]
            msg_4 = type_description[lang][24]
            msg_5 = type_description[lang][25]
            dispatcher.utter_message(msg_1)
            dispatcher.utter_message(msg_2)
            dispatcher.utter_message(msg_3)
            dispatcher.utter_message(msg_4)
            dispatcher.utter_message(msg_5)
        elif metadata["t"] == 4:
            h_type = type_description[lang][65] # 거울 종족
            msg_1 = type_description[lang][31]
            msg_2 = type_description[lang][32]
            msg_3 = type_description[lang][33]
            dispatcher.utter_message(msg_1)
            dispatcher.utter_message(msg_2)
            dispatcher.utter_message(msg_3)



        message = type_description[lang][35].format(h_type)
        dispatcher.utter_message(message)

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
        lang = metadata['lang']

        leading_priority = tracker.get_slot('leading_priority')

        buttons = []

        if metadata["t"] == 0:

            buttons.append({"title": type_description[lang][37],
                            "payload": "/type_question{\"bot_question\":\"어떤 에너지를 가지고 있나요?\", \"context_index\": 1}"})
            buttons.append({"title": type_description[lang][38],
                            "payload": "/type_question{\"bot_question\":\"힘들 때 어떻게 해야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": type_description[lang][39],
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저의 전략은 뭔가요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][40],
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 1:

            buttons.append({"title": type_description[lang][41],
                            "payload": "/type_question{\"bot_question\":\"어떤 단점이 있을까요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][42],
                            "payload": "/type_question{\"bot_question\":\"힘들 때 어떻게 해야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": type_description[lang][43],
                            "payload": "/strategy_question{\"bot_question\":\"스피드 에너자이저의 전략은 뭔가요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][44],
                            "payload": "/strategy_question{\"bot_question\":\"에너자이저 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 2:
            buttons.append({"title": type_description[lang][45],
                            "payload": "/type_question{\"bot_question\":\"어떻게 살아가야 하나요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][46],
                            "payload": "/type_question{\"bot_question\":\"주변 사람들은 왜 저를 힘들게 할까요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][47],
                            "payload": "/strategy_question{\"bot_question\":\"혁신주도가의 전략은 무엇인가요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][48],
                            "payload": "/strategy_question{\"bot_question\":\"알림은 어떻게 해야하나요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][49],
                            "payload": "/strategy_question{\"bot_question\":\"혁신주도가 아이는 어떻게 키워야 하나요?\", \"context_index\": 1}"})
        elif metadata["t"] == 3:
            buttons.append({"title": type_description[lang][50],
                            "payload": "/type_question{\"bot_question\":\"어떻게 살아가야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": type_description[lang][51],
                            "payload": "/type_question{\"bot_question\":\"어떤 장점이 있을까요?\", \"context_index\": 1}"})
            buttons.append({"title": type_description[lang][52],
                            "payload": "/type_question{\"bot_question\":\"가이드 아이는 어떻게 키워야 하나요?\", \"context_index\": 1}"})
            buttons.append({"title": type_description[lang][53],
                            "payload": "/strategy_question{\"bot_question\":\"초대가 무엇인가요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][54],
                            "payload": "/strategy_question{\"bot_question\":\"초대를 받은 후 어떻게 해야하나요?\", \"context_index\": 0}"})
        elif metadata["t"] == 4:

            buttons.append({"title": type_description[lang][55],
                            "payload": "/type_question{\"bot_question\":\"어떻게 살아가야 하나요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][56],
                            "payload": "/strategy_question{\"bot_question\":\"거울 종족의 전략은 무엇인가요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][57],
                            "payload": "/strategy_question{\"bot_question\":\"한 달간 기다리지 않으면 안되나요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][58],
                            "payload": "/strategy_question{\"bot_question\":\"거울 종족의 기다림을 어떻게 도와줘야 하나요?\", \"context_index\": 0}"})
            buttons.append({"title": type_description[lang][59],
                            "payload": "/strategy_question{\"bot_question\":\"거울 종족 아이는 어떻게 키워야 하나요?\", \"context_index\": 0}"})
        buttons.append({"title": etc_description[lang][19], "payload": "/leading_more"}) # 질문 없어요
        dispatcher.utter_message(type_description[lang][36], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/23701.wav"
        })
        dispatcher.utter_message(buttons=buttons)

        return []
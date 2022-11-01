import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker
from rasa_sdk.events import FollowupAction
import pandas as pd

logger = logging.getLogger(__name__)

smalltalk_question_csv = pd.read_csv("./data/smalltalk_question.csv")
smalltalk_question = []
smalltalk_question.append(smalltalk_question_csv['korean'].values.tolist())
smalltalk_question.append(smalltalk_question_csv['english'].values.tolist())
smalltalk_question.append(smalltalk_question_csv['voiceID'].values.tolist())

smalltalk_answer_csv = pd.read_csv("./data/smalltalk_answer.csv")
smalltalk_answer = []
smalltalk_answer.append(smalltalk_answer_csv['korean'].values.tolist())
smalltalk_answer.append(smalltalk_answer_csv['english'].values.tolist())

ninei_members = [['', '민준', '반', '베리', '서원', '위니', '이든', '제원', '주형', '지호', '태훈'],
['', 'MIN JUN', 'VAHN', 'VARI', 'SEO WON', 'WINNIE', 'EDEN', 'JE WON','JOO HYOUNG','JI HO','TAE HUN']]


class ActionSmalltalkFirst(Action):
    def name(self) -> Text:
        return "action_smalltalk_first"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_smalltalk_first')

        metadata = extract_metadata_from_tracker(tracker)
        smalltalk_step = tracker.get_slot('smalltalk_step')
        ninei = metadata['member']
        lang = metadata['lang']
        voice_num = tracker.get_slot('voice_num')

        # buttons 요소 2개 이상
        if smalltalk_step in [3, 22, 25, 35, 38]:
            buttons = []
            if smalltalk_step == 3:
                question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[lang][ninei])
                vID = smalltalk_question[voice_num][smalltalk_step]
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID), "data": question
                })
                buttons.append(
                    {"title": smalltalk_answer[lang][3], "payload": "/change_smalltalk_step{\"smalltalk_step\":3}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][4], "payload": "/change_smalltalk_step{\"smalltalk_step\":4}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][5], "payload": "/change_smalltalk_step{\"smalltalk_step\":5}"}
                )
            elif smalltalk_step == 22:
                question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[lang][ninei])
                vID = smalltalk_question[voice_num][smalltalk_step]
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID), "data": question
                })
                buttons.append(
                    {"title": smalltalk_answer[lang][22], "payload": "/change_smalltalk_step{\"smalltalk_step\":24}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][23], "payload": "/change_smalltalk_step{\"smalltalk_step\":24}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][24], "payload": "/change_smalltalk_step{\"smalltalk_step\":24}"}
                )
            elif smalltalk_step == 25:
                question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[lang][ninei])
                vID = smalltalk_question[voice_num][smalltalk_step]
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID), "data": question
                })
                buttons.append(
                    {"title": smalltalk_answer[lang][25], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][26], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][27], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][28], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
            elif smalltalk_step == 35:
                question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[lang][ninei])
                vID = smalltalk_question[voice_num][smalltalk_step]
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID), "data": question
                })
                buttons.append(
                    {"title": smalltalk_answer[lang][35], "payload": "/change_smalltalk_step{\"smalltalk_step\":36}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][36], "payload": "/change_smalltalk_step{\"smalltalk_step\":36}"}
                )
            elif smalltalk_step == 38:
                question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[lang][ninei])
                vID = smalltalk_question[voice_num][smalltalk_step]
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID), "data": question
                })
                buttons.append(
                    {"title": smalltalk_answer[lang][38], "payload": "/change_smalltalk_step{\"smalltalk_step\":38}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][39], "payload": "/change_smalltalk_step{\"smalltalk_step\":39}"}
                )

            dispatcher.utter_message(buttons=buttons)

        # buttons 요소 없음
        elif smalltalk_step in [31, 33, 41, 42, 44]:
            question = smalltalk_question[lang][smalltalk_step].format(metadata["pn"], ninei_members[lang][ninei])
            vID = smalltalk_question[voice_num][smalltalk_step]

            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": question
            })

            return [FollowupAction(name="action_change_smalltalk_step")]

        # buttons 요소 1개
        else:
            question = smalltalk_question[lang][smalltalk_step].format(metadata["pn"], ninei_members[lang][ninei])
                
            vID = smalltalk_question[voice_num][smalltalk_step]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": question
            })

            buttons = [{"title": smalltalk_answer[lang][smalltalk_step],
                        "payload": "/change_smalltalk_step"}]

            dispatcher.utter_message(buttons=buttons)


class ActionChangeSmalltalkStep(Action):
    def name(self) -> Text:
        return "action_change_smalltalk_step"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('action_change_smalltalk_step')

        smalltalk_step = tracker.get_slot('smalltalk_step')

         # 첫인사 끝
        if smalltalk_step in[34] : #종료
            return [FollowupAction(name="action_start")]
        if smalltalk_step == 37: # 재방문 인사 끝
            return [FollowupAction(name="action_masterbot"),SlotSet("regreetings",1)]
        if smalltalk_step == 44:
            return [] # 마무리 인사 끝
        if smalltalk_step == 40:
            return [SlotSet("smalltalk_step", smalltalk_step + 3), FollowupAction(name="action_smalltalk_first")]
        if smalltalk_step == 41: # 실망한 경우, 슬롯 값 변경후 대기 --> action_masterbot에서 값을 받아서 재실행
            return [SlotSet("disappointed", 1)] 
        if smalltalk_step in range(38,40):
            return [SlotSet("smalltalk_step", smalltalk_step + 2), FollowupAction(name="action_smalltalk_first")]
        if smalltalk_step in range(3,6):
            return [SlotSet("smalltalk_step", smalltalk_step + 3), FollowupAction(name="action_smalltalk_first")]
        elif smalltalk_step in range(6, 9):
            return [SlotSet("smalltalk_step", 9), FollowupAction(name="action_smalltalk_first")]
        elif smalltalk_step == 10: # 나인아이 멤버 자기소개 단계일 때
            metadata = extract_metadata_from_tracker(tracker)
            ninei = metadata['member']
            return [SlotSet("smalltalk_step", smalltalk_step + ninei), FollowupAction(name="action_smalltalk_first")]
        elif smalltalk_step in range(11, 21):
            return [SlotSet("smalltalk_step", 21), FollowupAction(name="action_smalltalk_first")]


        return [SlotSet("smalltalk_step", smalltalk_step + 1), FollowupAction(name="action_smalltalk_first")]

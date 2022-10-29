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

ninei_members = ['민준', '반', '베리', '서원', '위니', '이든', '제원', '주형', '지호', '태훈']


class ActionSmalltalkFirst(Action):
    def name(self) -> Text:
        return "action_smalltalk_first"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_smalltalk_first')

        metadata = extract_metadata_from_tracker(tracker)
        smalltalk_step = tracker.get_slot('smalltalk_step')
        ninei = metadata['member']
        lang = metadata['lang']

        # 첫인사 끝
        if smalltalk_step == 10:
            return [FollowupAction(name='action_start')]

        # buttons 요소 2개 이상
        if smalltalk_step in [3]:
            buttons = []
            if smalltalk_step == 3:
                question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[ninei])
                vID = smalltalk_question[2][smalltalk_step]
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID), "data": question
                })
                buttons.append(
                    {"title": smalltalk_answer[lang][3], "payload": "/change_smalltalk_step{\"smalltalk_step\":5}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][4], "payload": "/change_smalltalk_step{\"smalltalk_step\":5}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][5], "payload": "/change_smalltalk_step{\"smalltalk_step\":5}"}
                )
            dispatcher.utter_message(buttons=buttons)
        # buttons 요소 1개
        else:
            question = smalltalk_question[lang][smalltalk_step].format(metadata["pn"], ninei_members[ninei])
                
            vID = smalltalk_question[2][smalltalk_step]
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

        return [SlotSet("smalltalk_step", smalltalk_step + 1), FollowupAction(name="action_smalltalk_first")]

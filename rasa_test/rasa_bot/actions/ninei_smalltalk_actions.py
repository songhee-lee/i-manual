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

smalltalk_answer_csv = pd.read_csv("./data/smalltalk_answer.csv")
smalltalk_answer = []
smalltalk_answer.append(smalltalk_answer_csv['korean'].values.tolist())
smalltalk_answer.append(smalltalk_answer_csv['english'].values.tolist())


class ActionSmalltalkFirst(Action):
    def name(self) -> Text:
        return "action_smalltalk_first"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_smalltalk_first')

        metadata = extract_metadata_from_tracker(tracker)
        smalltalk_step = tracker.get_slot('smalltalk_step')
        ninei = tracker.get_slot('ninei')
        lang = tracker.get_slot('lang')

        # 첫인사 끝
        if smalltalk_step == 10:
            return [FollowupAction(name='action_start')]

        # buttons 요소 2개 이상
        if smalltalk_step in [3]:
            buttons = []
            if smalltalk_step == 3:
                question = smalltalk_question[lang][smalltalk_step]
                dispatcher.utter_message(question)
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
            question = smalltalk_question[lang][smalltalk_step]
            dispatcher.utter_message(question)

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

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
        continue_smalltalk = tracker.get_slot('continue_smalltalk')

        if continue_smalltalk == 1 :
            smalltalk_step += 1

        # 첫인사 끝
        if smalltalk_step == 10 :
            return [FollowupAction(name='action_start')]

        # buttons 요소 2개 이상
        if smalltalk_step == 3 :
            return [SlotSet('smalltalk_step', 6), FollowupAction(name='action_smalltalk_first')]

        # buttons 요소 1개
        else:
            question = smalltalk_question[lang][smalltalk_step]

            dispatcher.utter_message(question)

            buttons = []
            buttons.append(
                {"title": smalltalk_answer[lang][smalltalk_step], "payload": "/smalltalk_first{\"continue_smalltalk\":1}"}
            )

            dispatcher.utter_message(buttons=buttons)

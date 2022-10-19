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

smalltalk_csv = pd.read_csv("./data/smalltalk.csv")
smalltalk = []
smalltalk.append(smalltalk_csv['korean'].values.tolist())
smalltalk.append(smalltalk_csv['english'].values.tolist())


class ActionSmalltalkFirst(Action):
    def name(self) -> Text:
        return "action_smalltalk_first"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_smalltalk_first')

        metadata = extract_metadata_from_tracker(tracker)
        smalltalk_step = tracker.get_slot('smalltalk_step')
        ninei = tracker.get_slot('ninei')
        lang = tracker.get_slot('lang')

        msg = ""

        # buttons 요소 2개 이상
        if smalltalk_step in [4, 8, 9, 16, 18]:
            buttons = []


        # ninei = metadata['ninei']

        return [FollowupAction(name='action_set_priority')]
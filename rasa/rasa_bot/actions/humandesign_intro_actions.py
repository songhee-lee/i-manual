import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, extract_metadata_from_data
from rasa_sdk.events import FollowupAction
logger = logging.getLogger(__name__)

class ActionSetPriority(Action): #맨 처음
    def name(self):
        return "action_set_priority"

    def run(self, dispatcher, tracker, domain):
        print('action_set_priority')

        #metadata = extract_metadata_from_tracker(tracker)
        metadata = extract_metadata_from_data(1)

        #se는 의식해 의식지구 무의식해 무의식지구
        #metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0],"se":[2,0,6], "t": 3, "p": 52, "d": 3}

        #이후 action_set_priority를 초기 action으로 한 뒤 주석 제거
        #dispatcher.utter_message(
        #    f'안녕하세요. {metadata["pn"]}님 아이매뉴얼 마스터 봇입니다. 나답게 살기 위한 여행은 즐겁게 하고 계신가요?')
        #dispatcher.utter_message(
        #    f'안녕하세요. 저는 아이메뉴얼 마스터 봇입니다. 저는 좀 더 나답게 사는 것을 도와드리기 위해 기다리고 있었어요. {metadata["pn"]}님의 메뉴얼 설명을 원하시면 "시작" 이라고 말해주세요!')

        #리딩 우선순위 정하는 부분
        leading_priority=[]
        if metadata["t"] in [2,3,4]:
            leading_priority.append(0)
        if metadata["p"] in [14, 25, 36, 41, 52, 63]:
            leading_priority.append(1)
        if metadata["d"] in [3, 4]:
            leading_priority.append(2)
        leading_priority.append(3)
        for i in range(3):
            if i not in leading_priority:
                leading_priority.append(i)

        #센터 우선순위 정하는 부분 미정의 부터로 수정
        center_priority = []
        #미정의 먼저
        for i in metadata['se']:
            if metadata['ct'][i]==0 and (metadata["ct"][i] not in center_priority):
                center_priority.append(i)
        #그다음 정의
        for i in metadata['se']:
            if metadata['ct'][i]==1 and (metadata["ct"][i] not in center_priority):
                center_priority.append(i)

        for i in [8, 7, 6, 5, 2, 4, 3, 1, 0]:
            if i not in center_priority:
                center_priority.append(i)
        return [SlotSet('leading_priority', leading_priority), SlotSet('center_priority', center_priority), SlotSet('step', 0), SlotSet('is_finished', False), SlotSet('center_step', 0)] #slot추가 필요

class ActionStart(Action):
    def name(self):
        return "action_start"

    def run(self, dispatcher, tracker, domain):
        print('action_start')
        leading_priority = tracker.get_slot('leading_priority')
        if leading_priority[0]==0:
            return [FollowupAction(name='action_leading_type_intro')]
        elif leading_priority[0]==1:
            return [FollowupAction(name='action_leading_profile_intro')]
        elif leading_priority[0]==2:
            return [FollowupAction(name='action_leading_definition_intro')]
        elif leading_priority[0]==3:
            return [FollowupAction(name='action_leading_centers_intro')]

        return []

class ActionStep(Action):
    def name(self):
        return "action_step"

    def run(self, dispatcher, tracker, domain):
        print('action_step')
        leading_priority = tracker.get_slot('leading_priority')
        is_finished = tracker.get_slot("is_finished")
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        if is_finished==True:
            return [FollowupAction(name='action_masterbot')] #masterbot에서 처리할 수 있게
        # is_finished 상태로 계속하면 끝내버리고, 끝났다고 알려줌

        else:
            if center_step < 8 and center_step !=0:
                return [FollowupAction(name='action_leading_centers_intro')]
            else:
                if step == 4:
                    return [SlotSet('is_finished', True), FollowupAction(name='action_last_message')]
                else:
                    if leading_priority[step]==0:
                        return [FollowupAction(name='action_leading_type_intro')]
                    elif leading_priority[step]==1:
                        return [FollowupAction(name='action_leading_profile_intro')]
                    elif leading_priority[step]==2:
                        return [FollowupAction(name='action_leading_definition_intro')]
                    elif leading_priority[step]==3:
                        return [FollowupAction(name='action_leading_centers_intro')]

        return []

class ActionMore(Action):
    def name(self):
        return "action_more"
        #leading_more -> action_more

    def run(self, dispatcher, tracker, domain):
        print('action_more')
        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        buttons = []
        buttons.append({"title": f'계속', "payload": "/leading_step"})
        buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
        dispatcher.utter_message(f'계속 할까요?', buttons=buttons)

        return []
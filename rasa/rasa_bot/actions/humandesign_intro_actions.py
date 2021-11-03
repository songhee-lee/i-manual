import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, extract_metadata_from_data
from rasa_sdk.events import FollowupAction
logger = logging.getLogger(__name__)
#추후 삭제
class ActionSetMetadata(Action):
    def name(self):
        return "action_set_metadata"

    def run(selfself, dispatcher, tracker, domain):
        print('action_set_metadata')
        return [SlotSet('select_metadata', 22)]

class ActionSetPriority(Action): #맨 처음
    def name(self):
        return "action_set_priority"

    def run(self, dispatcher, tracker, domain):
        print('action_set_priority')
        #metadata = extract_metadata_from_tracker(tracker)

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)

        #이후 action_set_priority를 초기 action으로 한 뒤 주석 제거
        #dispatcher.utter_message(
        #    f'{metadata["pn"]}님, 안녕하세요, 저는 당신이 어떤 사람인지 알려줄 마스터 봇 입니다. 자, 이제 당신에 대해 알아봅시다.')

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
            if metadata['ct'][i]==0 and (i not in center_priority):
                center_priority.append(i)
        #그다음 정의
        for i in metadata['se']:
            if metadata['ct'][i]==1 and (i not in center_priority):
                center_priority.append(i)

        for i in [8, 7, 6, 5, 2, 4, 3, 1, 0]:
            if i not in center_priority:
                center_priority.append(i)
        return [FollowupAction(name='action_start'), SlotSet('leading_priority', leading_priority), SlotSet('center_priority', center_priority), SlotSet('step', 0), SlotSet('is_finished', 0), SlotSet('center_step', 0), SlotSet('is_question', 0), SlotSet('center_type',center_priority[0]), SlotSet('center_question', 0), SlotSet('is_sentiment', 0)] #slot추가 필요

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
        if is_finished==1:
            return [FollowupAction(name='action_masterbot')] #masterbot에서 처리할 수 있게
        # is_finished 상태로 계속하면 끝내버리고, 끝났다고 알려줌

        else:
            if leading_priority[step-1]==3 and center_step < 9:
                return [FollowupAction(name='action_leading_centers_intro')]
            else:
                if step == 4:
                    return [SlotSet('is_finished', 1), FollowupAction(name='action_last_message')]
                else:
                    dispatcher.utter_message("자, 이제 다른 특징에 대해 알아봅시다")
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

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        #최종버전은 이부분으로!
        #if center_step == 0 or center_step == 9:
        #    if step == 4:
        #        return [SlotSet('is_finished', 1), FollowupAction(name='action_last_message')]
        #    else:
        #        buttons = []
        #        buttons.append({"title": f'계속', "payload": "/leading_step"})
        #        buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
        #        dispatcher.utter_message(f'계속 할까요?', buttons=buttons)

        #이 밑부터 다 지우기
        if center_step==0 or center_step==9:
            if step == 4:
                return [SlotSet('is_finished', 1), FollowupAction(name='action_last_message')]
            else:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(f'계속 할까요?', buttons=buttons)
        else:
            if metadata["se"][0] in center_priority[0:center_step] and metadata["se"][1] in center_priority[0:center_step] and \
                    metadata["se"][2] in center_priority[0:center_step] and metadata["se"][3] in center_priority[0:center_step]:
                buttons = []
                buttons.append({"title": f'센터 건너뛰기', "payload": "/leading_drop_center"})
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(f'센터에 대한 설명을 이어서 들으시겠어요?', buttons=buttons)
            else:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(f'계속 할까요?', buttons=buttons)

        return []

#실제로는 지우기!
class ActionDropCenter(Action):
    def name(self):
        return "action_drop_center"
        #leading_more -> action_more

    def run(self, dispatcher, tracker, domain):
        print('action_drop_center')
        leading_priority = tracker.get_slot('leading_priority')

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        if step==4:
            return[FollowupAction(name='action_last_message'), SlotSet('center_step', 0), SlotSet('is_finished', 1)]
        else:
            if leading_priority[step] == 0:
                return [FollowupAction(name='action_leading_type_intro'), SlotSet('center_step', 0)]
            elif leading_priority[step] == 1:
                return [FollowupAction(name='action_leading_profile_intro'), SlotSet('center_step', 0)]
            elif leading_priority[step] == 2:
                return [FollowupAction(name='action_leading_definition_intro'), SlotSet('center_step', 0)]

        return []
import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker
from rasa_sdk.events import FollowupAction
from pymongo import MongoClient

# MongoDB setting
my_client = MongoClient("mongodb://localhost:27017/")
mydb = my_client['i-Manual']  # i-Manaul database 생성
mycol = mydb['users']  # users Collection 생성

logger = logging.getLogger(__name__)
import pandas as pd

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = etc_description_csv['paragraph'].values.tolist()


def change_gate_to_center(gate):
    se_gates = [gate[0], gate[1], gate[13], gate[14]]
    center = {0: [53, 60, 52, 19, 39, 41, 54, 38, 58],
              1: [5, 14, 29, 34, 27, 42, 3, 9, 59],
              2: [48, 57, 44, 50, 32, 28, 18],
              3: [37, 22, 36, 6, 49, 55, 30],
              4: [21, 51, 26, 40],
              5: [7, 1, 13, 25, 46, 2, 15, 10],
              6: [62, 23, 56, 35, 12, 45, 33, 8, 31, 20, 16],
              7: [47, 24, 4, 17, 43, 11],
              8: [64, 61, 63]
              }
    se = []
    for gt in se_gates:
        for i in range(0, 9):
            center_gates = center[i]
            if gt in center_gates:
                se.append(i)
                break
    return se


class ActionSetPriority(Action):  # 맨 처음
    def name(self):
        return "action_set_priority"

    def run(self, dispatcher, tracker, domain):
        print('action_set_priority')
        metadata = extract_metadata_from_tracker(tracker)
        print("metadata 출력")
        print(metadata)
        gt = metadata["gt"]
        se = change_gate_to_center(gt)
        message = etc_description[0].format(metadata["pn"])
        dispatcher.utter_message(
            message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10101.wav"
            }
        )

        # 리딩 우선순위 정하는 부분
        leading_priority = []
        if metadata["t"] in [2, 3, 4]:
            leading_priority.append(0)
        if metadata["p"] in [14, 25, 36, 41, 52, 63]:
            leading_priority.append(1)
        if metadata["d"] in [3, 4]:
            leading_priority.append(2)
        leading_priority.append(3)
        for i in range(3):
            if i not in leading_priority:
                leading_priority.append(i)

        # 센터 우선순위 정하는 부분 미정의 부터로 수정
        center_priority = []
        # 미정의 먼저
        for i in se:
            if metadata['ct'][i] == 0 and (i not in center_priority):
                center_priority.append(i)
        # 그다음 정의
        for i in se:
            if metadata['ct'][i] == 1 and (i not in center_priority):
                center_priority.append(i)

        for i in [8, 7, 6, 5, 2, 4, 3, 1, 0]:
            if i not in center_priority:
                center_priority.append(i)

        # check a user if he is new user
        x = mycol.find_one({"displayName": metadata["pn"]})
        if not x:
            mycol.insert_one({"displayID": metadata["uID"], "displayName": metadata["pn"], "type": metadata["t"],
                              "profile": metadata["p"],
                              "definition": metadata["d"], "centers": metadata["ct"], "question": [],
                              "self_notSelf": []})

        return [FollowupAction(name='action_start'), SlotSet('leading_priority', leading_priority),
                SlotSet('center_priority', center_priority),
                SlotSet('step', 0), SlotSet('is_finished', 0), SlotSet('center_step', 0), SlotSet('is_question', 0),
                SlotSet('center_type', center_priority[0]),
                SlotSet('center_question', 0), SlotSet('is_sentiment', 0),
                SlotSet('ego_or_unego', [0, 0, 0, 0, 0, 0, 0, 0, 0]), SlotSet('se', se)]  # slot추가 필요


class ActionSetPriorityAgain(Action):  # 맨 처음
    def name(self):
        return "action_set_priority_again"

    def run(self, dispatcher, tracker, domain):
        print('action_set_priority_again')
        metadata = extract_metadata_from_tracker(tracker)
        print("metadata 출력")
        print(metadata)
        gt = metadata["gt"]
        se = change_gate_to_center(gt)

        step = tracker.get_slot("step")
        is_finished = tracker.get_slot("is_finished")
        center_step = tracker.get_slot("center_step")
        is_question = tracker.get_slot("is_question")
        center_type = tracker.get_slot("center_type")
        center_question = tracker.get_slot("center_question")
        is_sentiment = tracker.get_slot("is_sentiment")
        ego_or_unego = tracker.get_slot("ego_or_unego")

        # 리딩 우선순위 정하는 부분
        leading_priority = []
        if metadata["t"] in [2, 3, 4]:
            leading_priority.append(0)
        if metadata["p"] in [14, 25, 36, 41, 52, 63]:
            leading_priority.append(1)
        if metadata["d"] in [3, 4]:
            leading_priority.append(2)
        leading_priority.append(3)
        for i in range(3):
            if i not in leading_priority:
                leading_priority.append(i)

        # 센터 우선순위 정하는 부분 미정의 부터로 수정
        center_priority = []
        # 미정의 먼저
        for i in se:
            if metadata['ct'][i] == 0 and (i not in center_priority):
                center_priority.append(i)
        # 그다음 정의
        for i in se:
            if metadata['ct'][i] == 1 and (i not in center_priority):
                center_priority.append(i)

        for i in [8, 7, 6, 5, 2, 4, 3, 1, 0]:
            if i not in center_priority:
                center_priority.append(i)

        if step is None:
            step = 0
        if is_finished is None:
            is_finished = 0
        if center_step is None:
            center_step = 0
        if is_question is None:
            is_question = 0
        if center_type is None:
            center_type = center_priority[0]
        if center_question is None:
            center_question = 0
        if is_sentiment is None:
            is_sentiment = 0
        if ego_or_unego is None:
            ego_or_unego = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # check a user if he is new user
        x = mycol.find_one({"displayName": metadata["pn"]})
        if not x:
            mycol.insert_one({"displayID": metadata["uID"], "displayName": metadata["pn"], "type": metadata["t"],
                              "profile": metadata["p"],
                              "definition": metadata["d"], "centers": metadata["ct"], "question": [],
                              "self_notSelf": []})

        return [FollowupAction(name='action_step'), SlotSet('leading_priority', leading_priority),
                SlotSet('center_priority', center_priority),
                SlotSet('step', step), SlotSet('is_finished', is_finished), SlotSet('center_step', center_step),
                SlotSet('is_question', is_question), SlotSet('center_type', center_type),
                SlotSet('center_question', center_question), SlotSet('is_sentiment', is_sentiment),
                SlotSet('ego_or_unego', ego_or_unego), SlotSet('se', se)]  # slot추가 필요


class ActionStart(Action):
    def name(self):
        return "action_start"

    def run(self, dispatcher, tracker, domain):
        print('action_start')
        leading_priority = tracker.get_slot('leading_priority')
        if leading_priority is None:
            return [FollowupAction(name='action_set_priority_again')]
        if leading_priority[0] == 0:
            return [FollowupAction(name='action_leading_type_intro')]
        elif leading_priority[0] == 1:
            return [FollowupAction(name='action_leading_profile_intro')]
        elif leading_priority[0] == 2:
            return [FollowupAction(name='action_leading_definition_intro')]
        elif leading_priority[0] == 3:
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
        metadata = extract_metadata_from_tracker(tracker)
        if leading_priority is None or is_finished is None or step is None or center_step is None:
            return [FollowupAction(name='action_set_priority_again')]
        if is_finished == 1:
            return [FollowupAction(name='action_masterbot')]  # masterbot에서 처리할 수 있게
        # is_finished 상태로 계속하면 끝내버리고, 끝났다고 알려줌

        else:
            if leading_priority[step - 1] == 3 and center_step < 9:
                return [FollowupAction(name='action_leading_centers_intro')]
            else:
                # 절전모드일때 step 건너뛰기
                if step < 4:
                    if leading_priority[step] == 2 and metadata["d"] == 0:
                        return [SlotSet('step', step + 1), FollowupAction(name='action_step')]
                if step == 4:
                    # is_finished = 1 은 last_message 나오고 set
                    return [FollowupAction(name='action_last_message')]
                else:
                    dispatcher.utter_message(etc_description[3], json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10401.wav"
                    })
                    if leading_priority[step] == 0:
                        return [FollowupAction(name='action_leading_type_intro')]
                    elif leading_priority[step] == 1:
                        return [FollowupAction(name='action_leading_profile_intro')]
                    elif leading_priority[step] == 2:
                        return [FollowupAction(name='action_leading_definition_intro')]
                    elif leading_priority[step] == 3:
                        return [FollowupAction(name='action_leading_centers_intro')]

        return []


class ActionMore(Action):
    def name(self):
        return "action_more"
        # leading_more -> action_more

    def run(self, dispatcher, tracker, domain):
        print('action_more')
        leading_priority = tracker.get_slot('leading_priority')

        metadata = extract_metadata_from_tracker(tracker)
        is_finished = tracker.get_slot("is_finished")
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        se = tracker.get_slot('se')
        if is_finished is None or step is None or center_step is None or center_priority is None or se is None:
            return [FollowupAction(name='action_set_priority_again')]

        if center_step == 0 or center_step == 9:
            if step == 4 and is_finished == 0:
                # is_finished = 1 은 last_message 나오고 set
                return [SlotSet('center_step', 0), FollowupAction(name='action_last_message')]
            else:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(etc_description[1], json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10201.wav"
                })
                dispatcher.utter_message(buttons=buttons)  #
        else:
            if se[0] in center_priority[0:center_step] and se[1] in center_priority[0:center_step] and \
                    se[2] in center_priority[0:center_step] and se[3] in center_priority[
                                                                         0:center_step] and is_finished == 0:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                buttons.append({"title": f'센터 건너뛰기', "payload": "/leading_drop_center"})
                dispatcher.utter_message(etc_description[2], json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10301.wav"
                })
                dispatcher.utter_message(buttons=buttons)
            else:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(etc_description[1], json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10201.wav"
                })
                dispatcher.utter_message(buttons=buttons)  #

        return []


class ActionDropCenter(Action):
    def name(self):
        return "action_drop_center"
        # leading_more -> action_more

    def run(self, dispatcher, tracker, domain):
        print('action_drop_center')
        leading_priority = tracker.get_slot('leading_priority')
        metadata = extract_metadata_from_tracker(tracker)
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        if leading_priority is None or step is None:
            return [FollowupAction(name='action_set_priority_again')]
        if step == 4:
            return [FollowupAction(name='action_last_message'), SlotSet('center_step', 0)]
        else:
            dispatcher.utter_message(etc_description[3], json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10401.wav"
            })
            if leading_priority[step] == 0:
                return [FollowupAction(name='action_leading_type_intro'), SlotSet('center_step', 0)]
            elif leading_priority[step] == 1:
                return [FollowupAction(name='action_leading_profile_intro'), SlotSet('center_step', 0)]
            elif leading_priority[step] == 2:
                return [FollowupAction(name='action_leading_definition_intro'), SlotSet('center_step', 0)]

        return []
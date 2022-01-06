<<<<<<< HEAD
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
    
class ActionSetPriority(Action): #맨 처음
    def name(self):
        return "action_set_priority"

    def run(self, dispatcher, tracker, domain):
        print('action_set_priority')
        metadata = extract_metadata_from_tracker(tracker)
        print("metadata 출력")
        print(metadata)
        gt = metadata["gt"]
        se = change_gate_to_center(gt)
        dispatcher.utter_message(
            f'{metadata["pn"]}님, 안녕하세요, 저는 당신이 어떤 사람인지 알려줄 마스터 봇 입니다. 자, 이제 당신에 대해 알아봅시다.')

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
        for i in se:
            if metadata['ct'][i]==0 and (i not in center_priority):
                center_priority.append(i)
        #그다음 정의
        for i in se:
            if metadata['ct'][i]==1 and (i not in center_priority):
                center_priority.append(i)

        for i in [8, 7, 6, 5, 2, 4, 3, 1, 0]:
            if i not in center_priority:
                center_priority.append(i)

        # check a user if he is new user
        x = mycol.find_one({"displayName": metadata["pn"]})
        if not x:
             mycol.insert_one({"displayID": metadata["uID"], "displayName": metadata["pn"], "type": metadata["t"], "profile": metadata["p"],
                               "definition": metadata["d"], "centers": metadata["ct"], "question": [],
                               "self_notSelf": []})

        return [FollowupAction(name='action_start'), SlotSet('leading_priority', leading_priority), SlotSet('center_priority', center_priority),
                SlotSet('step', 0), SlotSet('is_finished', 0), SlotSet('center_step', 0), SlotSet('is_question', 0), SlotSet('center_type',center_priority[0]),
                SlotSet('center_question', 0), SlotSet('is_sentiment', 0), SlotSet('ego_or_unego', [0, 0, 0, 0, 0, 0, 0, 0, 0]), SlotSet('se', se)] #slot추가 필요

class ActionSetPriorityAgain(Action): #맨 처음
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
        metadata = extract_metadata_from_tracker(tracker)
        if leading_priority is None or is_finished is None or step is None or center_step is None:
            return [FollowupAction(name='action_set_priority_again')]
        if is_finished==1:
            return [FollowupAction(name='action_masterbot')] #masterbot에서 처리할 수 있게
        # is_finished 상태로 계속하면 끝내버리고, 끝났다고 알려줌

        else:
            if leading_priority[step-1]==3 and center_step < 9:
                return [FollowupAction(name='action_leading_centers_intro')]
            else:
                # 절전모드일때 step 건너뛰기
                if step < 4:
                    if leading_priority[step] == 2 and metadata["d"] == 0:
                        return [SlotSet('step', step+1), FollowupAction(name='action_step')]
                if step == 4:
                    # is_finished = 1 은 last_message 나오고 set
                    return [FollowupAction(name='action_last_message')]
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

        metadata = extract_metadata_from_tracker(tracker)
        is_finished = tracker.get_slot("is_finished")
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        se = tracker.get_slot('se')
        if is_finished is None or step is None or center_step is None or center_priority is None or se is None:
            return [FollowupAction(name='action_set_priority_again')]

        if center_step==0 or center_step==9:
            if step == 4 and is_finished == 0:
                # is_finished = 1 은 last_message 나오고 set
                return [SlotSet('center_step', 0), FollowupAction(name='action_last_message')]
            else:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(f'계속 할까요?', buttons=buttons)
        else:
            if se[0] in center_priority[0:center_step] and se[1] in center_priority[0:center_step] and \
                    se[2] in center_priority[0:center_step] and se[3] in center_priority[0:center_step] and is_finished==0:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                buttons.append({"title": f'센터 건너뛰기', "payload": "/leading_drop_center"})
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

        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        if leading_priority is None or step is None:
            return [FollowupAction(name='action_set_priority_again')]
        if step==4:
            return[FollowupAction(name='action_last_message'), SlotSet('center_step', 0)]
        else:
            dispatcher.utter_message("자, 이제 다른 특징에 대해 알아봅시다")
            if leading_priority[step] == 0:
                return [FollowupAction(name='action_leading_type_intro'), SlotSet('center_step', 0)]
            elif leading_priority[step] == 1:
                return [FollowupAction(name='action_leading_profile_intro'), SlotSet('center_step', 0)]
            elif leading_priority[step] == 2:
                return [FollowupAction(name='action_leading_definition_intro'), SlotSet('center_step', 0)]

        return []
=======
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

    def run(self, dispatcher, tracker, domain):
        print('action_set_metadata')
        dispatcher.utter_message(f'내담자님의 정보를 입력해주세요')
        return [FollowupAction(name='action_listen')]
        #return [SlotSet('select_metadata', 1)] #10개의 특별한 케이스

class ActionSetMetadata2(Action):
    def name(self):
        return "action_set_metadata2"

    def run(self, dispatcher, tracker, domain):
        print('action_set_metadata2')
        user_text = tracker.latest_message['text']
        user_text = user_text.split("/")
        if user_text[1]=="에너자이저":
            user_text[1]=0
        elif user_text[1]=="스피드 에너자이저" or user_text[1]=="스피드에너자이저":
            user_text[1]=1
        elif user_text[1]=="혁신주도가" or user_text[1]=="매니페스터":
            user_text[1]=2
        elif user_text[1]=="가이드":
            user_text[1]=3
        elif user_text[1]=="거울":
            user_text[1]=4
        user_text[2] = int(user_text[2])
        user_text[3] = int(user_text[3])
        user_text[4] = user_text[4].split(',')
        user_text[4] = list(map(int, user_text[4]))
        user_text[5] = user_text[5].split(',')
        user_text[5] = list(map(int, user_text[5]))
        print("pn = ", user_text[0])
        print("t = ", user_text[1])
        print("p = ", user_text[2])
        print("d = ", user_text[3])
        print("ct = ", user_text[4])
        print("se = ", user_text[5])
        return [FollowupAction(name='action_set_priority'), SlotSet("pn", user_text[0]), SlotSet("t", user_text[1]), SlotSet("p", user_text[2]), SlotSet("d", user_text[3]), SlotSet("ct", user_text[4]), SlotSet("se", user_text[5])]
class ActionSetPriority(Action): #맨 처음
    def name(self):
        return "action_set_priority"

    def run(self, dispatcher, tracker, domain):
        print('action_set_priority')
        #metadata = extract_metadata_from_tracker(tracker)

        #select_metadata = tracker.get_slot('select_metadata')
        #metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

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

        #metadata = extract_metadata_from_tracker(tracker)
        #select_metadata = tracker.get_slot('select_metadata')
        #metadata = extract_metadata_from_data(select_metadata)

        metadata = extract_metadata_from_data(tracker)
        is_finished = tracker.get_slot("is_finished")
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
            if step == 4 and is_finished == 0:
                return [SlotSet('is_finished', 1), FollowupAction(name='action_last_message')]
            else:
                buttons = []
                buttons.append({"title": f'계속', "payload": "/leading_step"})
                buttons.append({"title": f'오늘은 그만', "payload": "/last_message"})
                dispatcher.utter_message(f'계속 할까요?', buttons=buttons)
                if center_step == 9:
                    return [SlotSet("center_step", 0)]
        else:
            if metadata["se"][0] in center_priority[0:center_step] and metadata["se"][1] in center_priority[0:center_step] and \
                    metadata["se"][2] in center_priority[0:center_step] and metadata["se"][3] in center_priority[0:center_step] and is_finished==0:
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

        #select_metadata = tracker.get_slot('select_metadata')
        #metadata = extract_metadata_from_data(select_metadata)

        metadata = extract_metadata_from_data(tracker)

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
>>>>>>> 6e5b3ffde30fb9df527bca3ab1846a7082a50ed2

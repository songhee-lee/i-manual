import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker
from rasa_sdk.events import FollowupAction
from pymongo import MongoClient

logger = logging.getLogger(__name__)

# MongoDB setting
my_client = MongoClient("mongodb://localhost:27017/")
mydb = my_client['i-Manual']  # i-Manaul database 생성
mycol2 = mydb['user_slot'] # user_slot Collection 


class ActionInitialized(Action):
    def name(self) -> Text:
        return "action_initialized"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_initialized')
        print(tracker.latest_message)
        # dispatcher.utter_message("로케이션 세팅 완료!")
        metadata = extract_metadata_from_tracker(tracker)

        return [FollowupAction(name='action_set_priority')]

class ActionLastMessage(Action):
    def name(self) -> Text:
        return "action_last_message"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_last_message')

        response = tracker.get_slot('result')
        print(response)
        metadata = extract_metadata_from_tracker(tracker)

        is_finished = tracker.get_slot('is_finished')
        if is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]
        
        # Save user's slot data in DB
        mycol2.update({"displayName": metadata["pn"]}, {"displayID": metadata["uID"], "displayName": metadata["pn"], 
                              "leading_priority" : tracker.get_slot("leading_priority"), "center_priority" : tracker.get_slot("center_priority"),
                              "step" : tracker.get_slot("step"), "is_finished":tracker.get_slot("is_finished"), "center_step":tracker.get_slot("center_step"), 
                              "center_type":tracker.get_slot("center_type")
                             }, upsert=True)
        
        if is_finished == 1:
            dispatcher.utter_message("마스터봇의 설명이 도움이 되고 있나요? 언제든 다시 불러주세요~")
        else:
            dispatcher.utter_message("당신이 타고난 디자인에 대한 마스터봇의 설명이 이해가 잘 되셨나요?")
            dispatcher.utter_message('아이매뉴얼에서 준비한 당신의 설명서를 꼼꼼히 읽어보시길 바랍니다."더불어 행복설명서와 관계사용 설명서도 꼭 읽어보세요~"')
            dispatcher.utter_message("궁금한 점이 있다면 언제든 다시 마스터봇을 불러주세요")
            dispatcher.utter_message("당신이 타고난 디자인대로 행복하게 살 수 있기를 응원합니다. 다시 만나요~")
            return [SlotSet('is_finished', 1)]

        
        return []

class ActionMasterbot(Action): #수정필요 entity를 통해 어디부분부터 설명할지
    def name(self) -> Text:
        return "action_masterbot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        
        metadata = extract_metadata_from_tracker(tracker)
        x = mycol2.find_one({"displayID": metadata["uID"]})
        leading_priority = tracker.get_slot("leading_priority")
        step = tracker.get_slot("step")
        is_finished = tracker.get_slot("is_finished")
        user_text = tracker.latest_message['text']
        center_step = tracker.get_slot('center_step')
        new_user = tracker.get_slot('new_user')
        # 처음들어온 user 가 마스터봇 호출할 경우

        if(user_text == "마스터 봇" or user_text == "마스터봇"):
            dispatcher.utter_message(
                f'안녕하세요 {metadata["pn"]}님, 저를 부르셨나요~? :) 다시 찾아주셔서 감사해요~')
        if leading_priority is None or step is None:
            if not x:
                return [FollowupAction(name='action_set_priority_again')]

        #다시 들어왔을 때 판단
        if is_finished==1:

            buttons = []
            buttons.append({"title": "종족", "payload": "/leading_type_intro"})
            buttons.append({"title": "사회적 성향", "payload": "/leading_profile_intro"})
            if metadata["d"] != 0:
                buttons.append({"title": "에너지 흐름", "payload": "/leading_definition_intro"})
            buttons.append({"title": "센터", "payload": "/leading_centers_intro"})
        
            dispatcher.utter_message("다시 듣고 싶은 항목을 선택해 주세요", buttons=buttons)
        else:
            buttons = []
            buttons.append({"title": "네 이어서 들을래요", "payload": "/leading_masterbot_more"})
            buttons.append({"title": "아뇨! 처음부터 들을래요", "payload": "/initialized"})

            dispatcher.utter_message("지난번에 이어서 들으시겠어요?", buttons=buttons)
        
        # Update user's slot data
        # x = mycol2.find_one({"displayID": metadata["uID"]})
        # if not x:        # 마스터봇 최초 사용자
        #     return []
        # else:
        #     return [SlotSet('leading_priority', x['leading_priority']), SlotSet('center_priority', x['center_priority']),
        #         SlotSet('step', x['step']), SlotSet('is_finished', x['is_finished']), SlotSet('center_step', x['center_step']), SlotSet('is_question', 0),
        #         ] #slot 저장

            
        # dispatcher.utter_message("로케이션 세팅 완료!")


class ActionMasterbotMore(Action):  # 수정필요 entity를 통해 어디부분부터 설명할지
    def name(self) -> Text:
        return "action_masterbot_more"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']

        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot("leading_priority")
        step = tracker.get_slot("step")
        center_step = tracker.get_slot('center_step')
        if leading_priority is None or step is None or center_step is None:
            return [FollowupAction(name='action_set_priority_again')]

        if leading_priority[step - 1] == 3 and center_step < 9:
            return [FollowupAction(name='action_leading_centers_intro')]
        else:
            if step == 4:
                return [SlotSet('is_finished', 1), FollowupAction(name='action_last_message')]
            else:
                if leading_priority[step] == 0:
                    return [FollowupAction(name='action_leading_type_intro')]
                elif leading_priority[step] == 1:
                    return [FollowupAction(name='action_leading_profile_intro')]
                elif leading_priority[step] == 2:
                    return [FollowupAction(name='action_leading_definition_intro')]
                elif leading_priority[step] == 3:
                    return [FollowupAction(name='action_leading_centers_intro')]
        return []
        # dispatcher.utter_message("로케이션 세팅 완료!")

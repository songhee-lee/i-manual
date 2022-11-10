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
mycol2 = mydb['user_slot']  # user_slot Collection

import pandas as pd

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = []
etc_description.append(etc_description_csv['korean'].values.tolist())
etc_description.append(etc_description_csv['english'].values.tolist())
etc_description.append(etc_description_csv['voiceID'].values.tolist())

# small talk 영어는 없다고 가정 하에 진행
# smalltalk_csv = pd.read_csv("./data/smalltalk_question.csv")
# smalltalk_question = smalltalk_csv['paragraph'].values.tolist()

# English ver.
# etc_description_eng_csv = pd.read_csv("./data/기타_eng.csv")
# etc_description_eng = etc_description_csv['paragraph'].values.tolist()

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
        lang = metadata['lang']
        ninei = metadata['member']
        voice_num = tracker.get_slot('voice_num')

        is_finished = tracker.get_slot('is_finished')
        if is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]

        # Save user's slot data in DB
        mycol2.update({"displayName": metadata["pn"]}, {"displayID": metadata["uID"], "displayName": metadata["pn"],
                                                        "leading_priority": tracker.get_slot("leading_priority"),
                                                        "center_priority": tracker.get_slot("center_priority"),
                                                        "step": tracker.get_slot("step"),
                                                        "is_finished": tracker.get_slot("is_finished"),
                                                        "center_step": tracker.get_slot("center_step"),
                                                        "center_type": tracker.get_slot("center_type")
                                                        }, upsert=True)

        if is_finished == 1:
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(etc_description[voice_num][10])),
                "data": etc_description[lang][10]
            })
        else:
            
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(etc_description[voice_num][11])),
                "data": etc_description[lang][11]
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(etc_description[voice_num][12])),
                "data": etc_description[lang][12]
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(etc_description[voice_num][13])),
                "data": etc_description[lang][13]
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(etc_description[voice_num][14])),
                "data": etc_description[lang][14]
            })

            return [SlotSet('is_finished', 1),SlotSet('smalltalk_step',38), FollowupAction(name="action_smalltalk_first")] #끝인사

        '''else:
            dispatcher.utter_message(etc_description[11], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/11201.mp3"
            })
            dispatcher.utter_message(etc_description[12], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/11301.mp3"
            })
            dispatcher.utter_message(etc_description[13], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/11401.mp3"
            })
            dispatcher.utter_message(etc_description[14], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/11501.mp3"
            })'''

        return [SlotSet('smalltalk_step',38), FollowupAction(name="action_smalltalk_first")] #끝인사


class ActionMasterbot(Action):  # 수정필요 entity를 통해 어디부분부터 설명할지
    def name(self) -> Text:
        return "action_masterbot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']

        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']
        ninei = metadata['member']

        x = mycol2.find_one({"displayID": metadata["uID"]})
        leading_priority = tracker.get_slot("leading_priority")
        step = tracker.get_slot("step")
        is_finished = tracker.get_slot("is_finished")
        user_text = tracker.latest_message['text']
        center_step = tracker.get_slot('center_step')
        new_user = tracker.get_slot('new_user')
        regreetings = tracker.get_slot('regreetings')
        voice_num = tracker.get_slot('voice_num')
        # 처음들어온 user 가 마스터봇 호출할 경우

        if regreetings == 0: #재방문인데, 재방문 인사를 하지 않은 경우
            if (user_text == "마스터 봇" or user_text == "마스터봇"):
                if ninei ==0:
                    message = etc_description[lang][15].format(metadata["pn"])
                    vID = etc_description[voice_num][15]
                    dispatcher.utter_message(json_message={
                            "type": "voiceID", 'sender': metadata['uID'],
                            "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                            "data" : message
                    })
            return[FollowupAction(name="action_smalltalk_first"),SlotSet("smalltalk_step",35)]
        
        if leading_priority is None or step is None:
            if not x:
                return [FollowupAction(name='action_set_priority_again')]

        # 다시 들어왔을 때 판단
        if is_finished == 1:

            buttons = []
            buttons.append({"title": etc_description[lang][25], "payload": "/leading_type_intro"}) # 종족
            buttons.append\
                ({"title": etc_description[lang][26], "payload": "/leading_profile_intro"}) # 사회적 성향
            if metadata["d"] != 0:
                buttons.append({"title": etc_description[lang][27], "payload": "/leading_definition_intro"}) # 에너지 흐름
            buttons.append({"title": etc_description[lang][28], "payload": "/leading_centers_intro"}) # 센터
            
            vID = etc_description[voice_num][16]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                "data" : etc_description[lang][16]
            })

            dispatcher.utter_message(buttons=buttons)

        else:
            buttons = []
            buttons.append({"title": etc_description[lang][29], "payload": "/leading_masterbot_more"}) # 네 이어서 들을래요
            buttons.append({"title": etc_description[lang][30], "payload": "/initialized"}) # 아뇨! 처음부터 들을래요

            vID = etc_description[voice_num][17]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                "data" : etc_description[lang][17]
            })

            dispatcher.utter_message(buttons=buttons)

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
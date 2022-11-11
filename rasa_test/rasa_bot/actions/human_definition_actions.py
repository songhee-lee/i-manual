import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker
from rasa_sdk.events import FollowupAction

logger = logging.getLogger(__name__)
import pandas as pd

definition_description_csv = pd.read_csv("./data/definition_description.csv")
definition_description = []
definition_description.append(definition_description_csv['korean'].values.tolist())
definition_description.append(definition_description_csv['english'].values.tolist())
definition_description.append(definition_description_csv['voiceID'].values.tolist())


class ActionLeadingDefinitionIntro(Action):
    def name(self) -> Text:
        return "action_leading_definition_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_definition_intro')

        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']
        ninei = metadata['member']
        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        is_finished = tracker.get_slot('is_finished')
        voice_num = tracker.get_slot('voice_num')

        if leading_priority is None or step is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]

        if is_finished == 1:
            dispatcher.utter_message(
                json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(definition_description[voice_num][0])), 
                    "data" : definition_description[lang][0]
                })

        if (metadata["d"] == 0):
             dispatcher.utter_message(
                json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(definition_description[voice_num][22])), 
                    "data" : definition_description[lang][22]
                })
        elif (metadata["d"] == 1):
            dispatcher.utter_message(
                json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(definition_description[voice_num][1])), 
                    "data" : definition_description[lang][1]
                })
        elif (metadata["d"] == 2):
            dispatcher.utter_message(
                json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(definition_description[voice_num][2])), 
                    "data" : definition_description[lang][2]
                })
        elif (metadata["d"] == 3):
            dispatcher.utter_message(
                json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(definition_description[voice_num][3])), 
                    "data" : definition_description[lang][3]
                })
        elif (metadata["d"] == 4):
            dispatcher.utter_message(
                json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(definition_description[voice_num][4])), 
                    "data" : definition_description[lang][4]
                })

        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        h_type = ''
        if metadata["d"] == 0:
            h_type = definition_description[lang][23] # 절전모드
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_0.png"
            # msg = "절전모드 간단한 설명입니다."
            # msg2 = "앞 부분 설명"
            msg3 = definition_description[lang][28]
            vID3 = definition_description[voice_num][28]
            msg4 = definition_description[lang][29]
            vID4 = definition_description[voice_num][29]
            msg5 = definition_description[lang][30]
            vID5 = definition_description[voice_num][30]
            tag = "카멜레온,무한한 잠재성,틈틈이 휴식할 것"
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            '''
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID), "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2), "data" : msg2
                })
            '''
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)), 
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)), 
                    "data" : msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)), 
                    "data" : msg5
                })
            message = definition_description[lang][21].format(h_type)
            vID = 4037 + metadata["d"]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'], 
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                "data" : message
            })
        elif metadata["d"] == 1:
            h_type = definition_description[lang][24] # 한 묶음 에너지 흐름
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_1.png"
            msg = definition_description[lang][5]
            vID = definition_description[voice_num][5]
            msg2 = definition_description[lang][6]
            vID2 = definition_description[voice_num][6]
            msg3 = definition_description[lang][7]
            vID3 = definition_description[voice_num][7]
            msg4 = definition_description[lang][8]
            vID4 = definition_description[voice_num][8]
            msg5 = definition_description[lang][9]
            vID5 = definition_description[voice_num][9]
            tag = "혼자서도 잘해요,조용하면 집중력 UP,홀로 공부할 것"
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)), 
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)), 
                    "data" : msg3
                })
            if msg4 != "":
                 dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)), 
                    "data" : msg4
                })
            if msg5 != "":
                 dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)), 
                    "data" : msg5
                })
            message = definition_description[lang][21].format(h_type)
            vID = 4037 + metadata["d"]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'], 
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                "data" : message
            })
        elif metadata["d"] == 2:
            h_type = definition_description[lang][25] # 두 묶음 에너지 흐름
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_2.png"
            msg = definition_description[lang][10]
            vID = definition_description[voice_num][10]
            msg2 = definition_description[lang][11]
            vID2 = definition_description[voice_num][11]
            msg3 = definition_description[lang][12]
            vID3 = definition_description[voice_num][12]

            tag = "카페에서도 공부 잘함,사람에 관심이 많아요,사람 많으면 아이디어 UP"
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)), 
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)), 
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)), 
                    "data" : msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)), 
                    "data" : msg5
                })
            message = definition_description[lang][21].format(h_type)
            vID = 4037 + metadata["d"]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'], 
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                "data" : message
            })
        elif metadata["d"] == 3:
            h_type = definition_description[lang][26] # 세 묶음 에너지 흐름
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_3.png"
            msg = definition_description[lang][13]
            vID = definition_description[voice_num][13]
            msg2 = definition_description[lang][14]
            vID2 = definition_description[voice_num][14]
            msg3 = definition_description[lang][15]
            vID3 = definition_description[voice_num][15]
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)), 
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)), 
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)), 
                    "data" : msg4
                }) 
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)), 
                    "data" : msg5
                }) 
            tag = "갈대같은 사람,한 곳에서 집중이 힘듦,자리를 바꿔 공부할 것"
            message = definition_description[lang][21].format(h_type)
            vID = 4037 + metadata["d"]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'], 
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                "data" : message
            })
        elif metadata["d"] == 4:
            h_type = definition_description[lang][27] # 네 묶음 에너지 흐름
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_4.png"
            msg = definition_description[lang][16]
            vID = definition_description[voice_num][16]
            msg2 = definition_description[lang][17]
            vID2 = definition_description[voice_num][17]
            msg3 = definition_description[lang][18]
            vID3 = definition_description[voice_num][18]
            msg4 = definition_description[lang][19]
            vID4 = definition_description[voice_num][19]
            msg5 = definition_description[lang][20]
            vID5 = definition_description[voice_num][20]
            tag = "우유부단,새로운게 필요해,친구들과 공부할 것"

            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)), 
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)), 
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)), 
                    "data" : msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], 
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)), 
                    "data" : msg5
                })

        # dispatcher.utter_message(json_message = {
        #                         "type": "arrContents", "content": [[msg, msg2], [msg3, msg4], [msg5]], "tags": f'{tag}'})

            message = definition_description[lang][21].format(h_type)
            vID = 4037 + metadata["d"]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'], 
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)), 
                "data" : message
            })

        if leading_priority[0] == 2:
            return [SlotSet('step', 1), FollowupAction(name='action_question_intro')]
        elif leading_priority[1] == 2:
            return [SlotSet('step', 2), FollowupAction(name='action_question_intro')]
        elif leading_priority[2] == 2:
            return [SlotSet('step', 3), FollowupAction(name='action_question_intro')]
        elif leading_priority[3] == 2:
            return [SlotSet('step', 4), FollowupAction(name='action_question_intro')]

import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, unego_get_question
from rasa_sdk.events import FollowupAction

center_leading_step = None
import pandas as pd

center_description_csv = pd.read_csv("./data/center_description.csv")
center_description = []
center_description.append(center_description_csv['korean'].values.tolist())
center_description.append(center_description_csv['english'].values.tolist())
center_description.append(center_description_csv['voiceID'].values.tolist())

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = []
etc_description.append(etc_description_csv['korean'].values.tolist())
etc_description.append(etc_description_csv['english'].values.tolist())
etc_description.append(etc_description_csv['voiceID'].values.tolist())

logger = logging.getLogger(__name__)


# 추후 밑에 클래스 복사해서 사용
class ActionLeadingCentersIntro(Action):
    def name(self) -> Text:
        return "action_leading_centers_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_intro')
        # 기존 priority = [4,3,5,2,6,0] # 에고 감정 방향 직관 표현 연료
        definedCnt = 0

        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']
        ninei = metadata['member']
        voice_num = tracker.get_slot('voice_num')

        print("MetaData: ", metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        is_finished = tracker.get_slot('is_finished')       #cycle을 다 들었을 때 1, 처음 들을때는 0
        if leading_priority is None or step is None or center_step is None or center_priority is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]
        if center_step == 9:
            if is_finished == 0:
                return [FollowupAction(name="action_more")]
            else:
                center_step = 0

        center_type = center_priority[center_step]
        if is_finished == 1:
            if center_step == 0:    # 센터 재설명
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][0]),
                    "data" : center_description[lang][0]
                })
        else:
            if center_step == 0:    # 센터 intro
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][1]),
                    "data" : center_description[lang][1]
                })
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][2]),
                    "data" : center_description[lang][2]
                })
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][3]),
                    "data" : center_description[lang][3]
                })
        # 연료센터
        if center_type == 0:

            if metadata['ct'][0] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][4]),
                    "data": center_description[lang][4]
                })
            elif metadata['ct'][0] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][5]),
                    "data": center_description[lang][5]
                })
        # 활력센터
        elif center_type == 1:

            if metadata['ct'][1] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][6]),
                    "data": center_description[lang][6]
                })
            elif metadata['ct'][1] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][7]),
                    "data": center_description[lang][7]
                })
        # 직관센터
        elif center_type == 2:
            if metadata['ct'][2] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][8]),
                    "data": center_description[lang][8]
                })
            elif metadata['ct'][2] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][9]),
                    "data": center_description[lang][9]
                })
        # 감정센터
        elif center_type == 3:
            if metadata['ct'][3] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][10]),
                    "data": center_description[lang][10]
                })
            elif metadata['ct'][3] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][11]),
                    "data": center_description[lang][11]
                })
        # 에고센터
        elif center_type == 4:
            if metadata['ct'][4] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][12]),
                    "data": center_description[lang][12]
                })
            elif metadata['ct'][4] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][13]),
                    "data": center_description[lang][13]
                })
        # 방향센터
        elif center_type == 5:
            if metadata['ct'][5] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][14]),
                    "data": center_description[lang][14]
                })
            elif metadata['ct'][5] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][15]),
                    "data" : center_description[lang][15]
                })

        # 표현센터
        elif center_type == 6:
            if metadata['ct'][6] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][16]),
                    "data": center_description[lang][16]
                })
            elif metadata['ct'][6] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][17]),
                    "data" : center_description[lang][17]
                })
        # 생각센터
        elif center_type == 7:
            if metadata['ct'][7] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][18]),
                    "data": center_description[lang][18]
                })
            elif metadata['ct'][7] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][19]),
                    "data" : center_description[lang][19]
                })
        # 영감센터
        elif center_type == 8:
            if metadata['ct'][8] == 0:      # 미정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][20]),
                    "data": center_description[lang][20]
                })
            elif metadata['ct'][8] == 1:    # 정의
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][21]),
                    "data" : center_description[lang][21]
                })

        for i in metadata['ct']:
            definedCnt += i

        if leading_priority[0] == 3:
            step = 1
        elif leading_priority[1] == 3:
            step = 2
        elif leading_priority[2] == 3:
            step = 3
        elif leading_priority[3] == 3:
            step = 4

        print("center_leading_step", center_leading_step)

        print("get Step")
        print(tracker.get_slot('step'))
        print("center step", tracker.get_slot('center_step'))
        print("get Step end")
        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        h_center = center_priority[center_step]  # 센터 몇번째까지 했는지를 기준으로 정하는 부분
        center_name = ""
        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            center_name = etc_description[lang][31]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/root.png"
            msg = center_description[lang][22]
            vID = center_description[voice_num][22]
            msg2 = center_description[lang][23]
            vID2 = center_description[voice_num][23]
            msg3 = center_description[lang][24]
            vID3 = center_description[voice_num][24]
            msg4 = center_description[lang][25]
            vID4 = center_description[voice_num][25]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })

        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            center_name = etc_description[lang][32]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/sacral.png"
            msg = center_description[lang][29]
            vID = center_description[voice_num][29]
            msg2 = center_description[lang][30]
            vID2 = center_description[voice_num][30]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if h_center == 1 or h_center == 7 or h_center == 8:
                message = center_description[lang][136].format(center_name) # 활력 센터
                vID = 5158 + h_center
                dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
                })
                return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                        SlotSet('step', step), FollowupAction(name='action_question_intro')]

        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            center_name = etc_description[lang][33]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/spleen.png"
            msg = center_description[lang][31]
            vID = center_description[voice_num][31]
            msg2 = center_description[lang][32]
            vID2 = center_description[voice_num][32]
            msg3 = center_description[lang][33]
            vID3 = center_description[voice_num][33]
            msg4 = center_description[lang][34]
            vID4 = center_description[voice_num][34]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })


        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            center_name = etc_description[lang][34]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/solar.png"
            msg = center_description[lang][40]
            vID = center_description[voice_num][40]
            msg2 = center_description[lang][41]
            vID2 = center_description[voice_num][41]
            msg3 = center_description[lang][42]
            vID3 = center_description[voice_num][42]
            msg4 = center_description[lang][43]
            vID4 = center_description[voice_num][43]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })



        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            center_name = etc_description[lang][35]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/heart.png"
            msg = center_description[lang][49]
            vID = center_description[voice_num][49]
            msg2 = center_description[lang][50]
            vID2 = center_description[voice_num][50]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })



        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            center_name = etc_description[lang][36]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/g.png"
            msg = center_description[lang][56]
            vID = center_description[voice_num][56]
            msg2 = center_description[lang][57]
            vID2 = center_description[voice_num][57]
            msg3 = center_description[lang][58]
            vID3 = center_description[voice_num][58]
            msg4 = center_description[lang][59]
            vID4 = center_description[voice_num][59]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })


        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            center_name = etc_description[lang][37]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/throat.png"
            msg = center_description[lang][66]
            vID = center_description[voice_num][66]
            msg2 = center_description[lang][67]
            vID2 = center_description[voice_num][67]
            msg3 = center_description[lang][68]
            vID3 = center_description[voice_num][68]
            msg4 = center_description[lang][69]
            vID4 = center_description[voice_num][69]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })


        elif h_center == 7 and metadata["ct"][7] == 1:
            h_type = "생각 센터 ( 정의 )"
            center_name = etc_description[lang][38]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/ajna.png"
            msg = center_description[lang][75]
            vID = center_description[voice_num][75]
            msg2 = center_description[lang][76]
            vID2 = center_description[voice_num][76]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if h_center == 1 or h_center == 7 or h_center == 8:
                message = center_description[lang][136].format(center_name) # 생각 센터
                vID = 5158 + h_center
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : message
                })
                return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                        SlotSet('step', step), FollowupAction(name='action_question_intro')]

        elif h_center == 8 and metadata["ct"][8] == 1:
            h_type = "영감 센터 ( 정의 )"
            center_name = etc_description[lang][39]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/head.png"
            msg = center_description[lang][77]
            vID = center_description[voice_num][77]
            msg2 = center_description[lang][78]
            vID2 = center_description[voice_num][78]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if h_center == 1 or h_center == 7 or h_center == 8:
                message = center_description[lang][136].format(center_name) # 영감센터
                vID = 5158 + h_center
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei,vID),
                    "data" : message
                })
                return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                        SlotSet('step', step), FollowupAction(name='action_question_intro')]

        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            center_name = etc_description[lang][31]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/root_off.png"
            msg = center_description[lang][79]
            vID = center_description[voice_num][79]
            msg2 = center_description[lang][80]
            vID2 = center_description[voice_num][80]
            msg3 = center_description[lang][81]
            vID3 = center_description[voice_num][81]
            msg4 = center_description[lang][82]
            vID4 = center_description[voice_num][82]
            msg5 = center_description[lang][83]
            vID5 = center_description[voice_num][83]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID5),
                "data": msg5
            })

        elif h_center == 1 and metadata['ct'][1] == 0:
            h_type = "활력 센터 ( 미정의 )"
            center_name = etc_description[lang][32]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/sacral_off.png"
            msg = center_description[lang][89]
            vID = center_description[voice_num][89]
            msg2 = center_description[lang][90]
            vID2 = center_description[voice_num][90]
            msg3 = center_description[lang][91]
            vID3 = center_description[voice_num][91]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if h_center == 1 or h_center == 7 or h_center == 8:
                message = center_description[lang][136].format(center_name) # 활력센터
                vID = 5158 + h_center
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data": message
                })
                return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                        SlotSet('step', step), FollowupAction(name='action_question_intro')]
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            center_name = etc_description[lang][33]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/spleen_off.png"
            msg = center_description[lang][92]
            vID = center_description[voice_num][92]
            msg2 = center_description[lang][93]
            vID2 = center_description[voice_num][93]
            msg3 = center_description[lang][94]
            vID3 = center_description[voice_num][94]
            msg4 = center_description[lang][95]
            vID4 = center_description[voice_num][95]
            msg5 = center_description[lang][96]
            vID5 = center_description[voice_num][96]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID5),
                "data": msg5
                })

        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            center_name = etc_description[lang][34]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/solar_off.png"
            msg = center_description[lang][101]
            vID = center_description[voice_num][101]
            msg2 = center_description[lang][102]
            vID2 = center_description[voice_num][102]
            msg3 = center_description[lang][103]
            vID3 = center_description[voice_num][103]
            msg4 = center_description[lang][104]
            vID4 = center_description[voice_num][104]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                    "data" : msg4
                })


        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            center_name = etc_description[lang][35]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/heart_off.png"
            msg = center_description[lang][110]
            vID = center_description[voice_num][110]
            msg2 = center_description[lang][111]
            vID2 = center_description[voice_num][111]
            msg3 = center_description[lang][112]
            vID3 = center_description[voice_num][112]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })



        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            center_name = etc_description[lang][36]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/g_off.png"
            msg = center_description[lang][119]
            vID = center_description[voice_num][119]
            msg2 = center_description[lang][120]
            vID2 = center_description[voice_num][120]
            msg3 = center_description[lang][121]
            vID3 = center_description[voice_num][121]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })

        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            center_name = etc_description[lang][37]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/throat_off.png"
            msg = center_description[lang][126]
            vID = center_description[voice_num][126]
            msg2 = center_description[lang][127]
            vID2 = center_description[voice_num][127]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })


        elif h_center == 7 and metadata['ct'][7] == 0:
            h_type = "생각 센터 ( 미정의 )"
            center_name = etc_description[lang][38]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/ajna_off.png"
            msg = center_description[lang][131]
            vID = center_description[voice_num][131]
            msg2 = center_description[lang][132]
            vID2 = center_description[voice_num][132]
            msg3 = center_description[lang][133]
            vID3 = center_description[voice_num][133]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                    "data" : msg3
                })
            if h_center == 1 or h_center == 7 or h_center == 8:
                message = center_description[lang][136].format(center_name) # 생각센터
                vID = 5158 + h_center
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data": message
                })
                return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                        SlotSet('step', step), FollowupAction(name='action_question_intro')]
        elif h_center == 8 and metadata['ct'][8] == 0:
            h_type = "영감 센터 ( 미정의 )"
            center_name = etc_description[lang][39]
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/head_off.png"
            msg = center_description[lang][134]
            vID = center_description[voice_num][134]
            msg2 = center_description[lang][135]
            vID2 = center_description[voice_num][135]
            dispatcher.utter_message(image=img)
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data" : msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                    "data" : msg2
                })
            if h_center == 1 or h_center == 7 or h_center == 8:
                message = center_description[lang][136].format(center_name) # 영감센터
                vID = 5158 + h_center
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                    "data": message
                })
                return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                        SlotSet('step', step), FollowupAction(name='action_question_intro')]


        return [SlotSet('center_step', center_step), SlotSet('center_type', h_center),
                SlotSet("step", step), FollowupAction(name='action_center_detail_intro')]


class ActionLeadingCenters(Action):
    def name(self) -> Text:
        return "action_leading_centers"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers')
        # 기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        definedCnt = 0

        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']
        ninei = metadata['member']
        print("MetaData: ", metadata)
        voice_num = tracker.get_slot('voice_num')

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        if leading_priority is None or step is None or center_step is None:
            return [FollowupAction(name='action_set_priority_again')]

        if center_step == 9:
            return [FollowupAction(name="action_more")]
        center_priority = tracker.get_slot('center_priority')

        if leading_priority[0] == 3:
            step = 1
        elif leading_priority[1] == 3:
            step = 2
        elif leading_priority[2] == 3:
            step = 3
        elif leading_priority[3] == 3:
            step = 4

        print("center_leading_step", center_leading_step)

        print("get Step")
        print(tracker.get_slot('step'))
        print("center step", tracker.get_slot('center_step'))
        print("get Step end")
        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        center_name = ""
        h_center = center_priority[center_step]  # 센터 몇번째까지 했는지를 기준으로 정하는 부분
        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            center_name = etc_description[lang][31]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = center_description[lang][27]
            vID = center_description[voice_num][27]
            msg2 = center_description[lang][28]
            vID2 = center_description[voice_num][28]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            message = center_description[lang][136].format(center_name) # 연료센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })


        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            center_name = etc_description[lang][33]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = center_description[lang][36]
            vID = center_description[voice_num][36]
            msg2 = center_description[lang][37]
            vID2 = center_description[voice_num][37]
            msg3 = center_description[lang][38]
            vID3 = center_description[voice_num][38]
            msg4 = center_description[lang][39]
            vID4 = center_description[voice_num][39]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data": msg4
            })

            message = center_description[lang][136].format(center_name) # 직관센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })
        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            center_name = etc_description[lang][34]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = center_description[lang][45]
            vID = center_description[voice_num][45]
            msg2 = center_description[lang][46]
            vID2 = center_description[voice_num][46]
            msg3 = center_description[lang][47]
            vID3 = center_description[voice_num][47]
            msg4 = center_description[lang][48]
            vID4 = center_description[voice_num][48]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data": msg4
            })
            message = center_description[lang][136].format(center_name) # 감정센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            center_name = etc_description[lang][35]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = center_description[lang][52]
            vID = center_description[voice_num][52]
            msg2 = center_description[lang][53]
            vID2 = center_description[voice_num][53]
            msg3 = center_description[lang][54]
            vID3 = center_description[voice_num][54]
            msg4 = center_description[lang][55]
            vID4 = center_description[voice_num][55]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data": msg4
            })
            message = center_description[lang][136].format(center_name) # 에고센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            center_name = etc_description[lang][36]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = center_description[lang][61]
            vID = center_description[voice_num][61]
            msg2 = center_description[lang][62]
            vID2 = center_description[voice_num][62]
            msg3 = center_description[lang][63]
            vID3 = center_description[voice_num][63]
            msg4 = center_description[lang][64]
            vID4 = center_description[voice_num][64]
            msg5 = center_description[lang][65]
            vID5 = center_description[voice_num][65]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data" : msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data" : msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data" : msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data" : msg4
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID5),
                "data" : msg5
            })

            message = center_description[lang][136].format(center_name) # 방향센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data" : message
            })
        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            center_name = etc_description[lang][37]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = center_description[lang][71]
            vID = center_description[voice_num][71]
            msg2 = center_description[lang][72]
            vID2 = center_description[voice_num][72]
            msg3 = center_description[lang][73]
            vID3 = center_description[voice_num][73]
            msg4 = center_description[lang][74]
            vID4 = center_description[voice_num][74]
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data" : msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data" : msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data" : msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data" : msg4
            })

            message = center_description[lang][136].format(center_name) # 표현센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data" : message
            })
        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            center_name = etc_description[lang][31]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            msg = center_description[lang][85]
            vID = center_description[voice_num][85]
            msg2 = center_description[lang][86]
            vID2 = center_description[voice_num][86]
            msg3 = center_description[lang][87]
            vID3 = center_description[voice_num][87]
            msg4 = center_description[lang][88]
            vID4 = center_description[voice_num][88]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data": msg4
            })
            
            message = center_description[lang][136].format(center_name) # 연료센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })

        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            center_name = etc_description[lang][33]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = center_description[lang][98]
            vID = center_description[voice_num][98]
            msg2 = center_description[lang][99]
            vID2 = center_description[voice_num][99]
            msg3 = center_description[lang][100]
            vID3 = center_description[voice_num][100]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            message = center_description[lang][136].format(center_name) # 직관센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })


        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            center_name = etc_description[lang][34]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = center_description[lang][106]
            vID = center_description[voice_num][106]
            msg2 = center_description[lang][107]
            vID2 = center_description[voice_num][107]
            msg3 = center_description[lang][108]
            vID3 = center_description[voice_num][108]
            msg4 = center_description[lang][109]
            vID4 = center_description[voice_num][109]
            
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data": msg4
            })
            message = center_description[lang][136].format(center_name) # 감정센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })

        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            center_name = etc_description[lang][35]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = center_description[lang][114]
            vID = center_description[voice_num][114]
            msg2 = center_description[lang][115]
            vID2 = center_description[voice_num][115]
            msg3 = center_description[lang][116]
            vID3 = center_description[voice_num][116]
            msg4 = center_description[lang][117]
            vID4 = center_description[voice_num][117]
            msg5 = center_description[lang][118]
            vID5 = center_description[voice_num][118]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID4),
                "data": msg4
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID5),
                "data": msg5
            })
            message = center_description[lang][136].format(center_name) # 에고센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            center_name = etc_description[lang][36]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = center_description[lang][123]
            vID = center_description[voice_num][123]
            msg2 = center_description[lang][124]
            vID2 = center_description[voice_num][124]
            msg3 = center_description[lang][125]
            vID3 = center_description[voice_num][125]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID3),
                "data": msg3
            })
            message = center_description[lang][136].format(center_name) # 방향센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": message
            })
        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            center_name = etc_description[lang][37]
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = center_description[lang][129]
            vID = center_description[voice_num][129]
            msg2 = center_description[lang][130]
            vID2 = center_description[voice_num][130]

            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data": msg
            })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID2),
                "data": msg2
            })

            message = center_description[lang][136].format(center_name) # 표현센터
            vID = 5158 + h_center
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                "content": "{0}/{1}/{2}.wav".format(lang, ninei, vID),
                "data" : message
            })

        return [SlotSet("is_question", 0), SlotSet("center_type", h_center), SlotSet("center_step", center_step),
                SlotSet("center_question", True), SlotSet("step", step), SlotSet("is_sentiment", True),
                FollowupAction(name="action_question_intro")]


class ActionLeadingCentersQuestion(Action):
    def name(self) -> Text:
        return "action_leading_centers_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_question')

        metadata = extract_metadata_from_tracker(tracker)

        print("MetaData: ", metadata)
        step = tracker.get_slot('step')
        if step is None:
            return [FollowupAction(name='action_set_priority_again')]

        return [SlotSet('step', step), SlotSet("center_question", False), FollowupAction(name='action_more')]


class ActionCenterDetailIntro(Action):
    def name(self) -> Text:
        return "action_center_detail_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_center_detail_intro')
        # 자세히 설명하기 위한 인트로 (센터별로 다르기때문에 새로 구현)
        metadata = extract_metadata_from_tracker(tracker)
        lang = metadata['lang']
        ninei = metadata['member']
        voice_num = tracker.get_slot('voice_num')

        center_step = tracker.get_slot("center_step")
        center_priority = tracker.get_slot('center_priority')

        if center_step is None or center_priority is None:
            return [FollowupAction(name='action_set_priority_again')]

        h_center = center_priority[center_step]

        buttons = []
        buttons.append({"title": center_description[lang][137], "payload": "/leading_centers"}) # 네 듣고싶어요
        buttons.append({"title": center_description[lang][138], "payload": "/question_intro"}) # 아뇨 괜찮아요

        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            dispatcher.utter_message(center_description[lang][26], buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            dispatcher.utter_message(center_description[lang][35], buttons=buttons)

        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            dispatcher.utter_message(center_description[lang][44], buttons=buttons)

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            dispatcher.utter_message(center_description[lang][51], buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                 "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][60]),
                 "data" : center_description[lang][60]
            })
            dispatcher.utter_message(buttons=buttons)

        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            dispatcher.utter_message(json_message={
                "type": "voiceID", 'sender': metadata['uID'],
                 "content": "{0}/{1}/{2}.wav".format(lang, ninei, center_description[voice_num][70]),
                 "data" : center_description[lang][70]
            })
            dispatcher.utter_message(buttons=buttons)



        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[lang][84], buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[lang][97], buttons=buttons)
        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[lang][105], buttons=buttons)
        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[lang][113], buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[lang][122], buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[lang][128], buttons=buttons)

        return []
# class ActionCenterMore(Action):
#    def name(self) -> Text:
#        return "action_center_more"

#    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        print('action_center_more')
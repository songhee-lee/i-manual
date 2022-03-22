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
center_description = center_description_csv['paragraph'].values.tolist()

logger = logging.getLogger(__name__)


# 추후 밑에 클래스 복사해서 사용
class ActionLeadingCentersIntro(Action):
    def name(self) -> Text:
        return "action_leading_centers_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_centers_intro')
        # 기존 priority = [4,3,5,2,6,0] #에고 감정 방향 직관 표현 연료
        definedCnt = 0

        metadata = extract_metadata_from_tracker(tracker)

        print("MetaData: ", metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        center_step = tracker.get_slot('center_step')
        center_priority = tracker.get_slot('center_priority')
        is_finished = tracker.get_slot('is_finished')
        if leading_priority is None or step is None or center_step is None or center_priority is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]
        if center_step == 9:
            if is_finished == 0:
                return [FollowupAction(name="action_more")]
            else:
                center_step = 0

        center_type = center_priority[center_step]
        if is_finished == 1:
            if center_step == 0:
                dispatcher.utter_message(
                    center_description[0], json_message={
                        "type": "voice", 'sender': metadata['uID'], "voiceid": "12", "voiceDuration": "123"
                    }
                )
        else:
            if center_step == 0:
                dispatcher.utter_message(
                    center_description[1], json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/5-2.wav"
                    }
                )
                dispatcher.utter_message(
                    center_description[2], json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/5-3.wav"
                    }
                )
                dispatcher.utter_message(
                    center_description[3], json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/5-4.wav"
                    }
                )
        # 연료센터
        if center_type == 0:

            if metadata['ct'][0] == 0:
                dispatcher.utter_message(
                    center_description[4])
            elif metadata['ct'][0] == 1:
                dispatcher.utter_message(
                    center_description[5])
        # 활력센터
        elif center_type == 1:

            if metadata['ct'][1] == 0:
                dispatcher.utter_message(
                    center_description[6])
            elif metadata['ct'][1] == 1:
                dispatcher.utter_message(
                    center_description[7])
        # 직관센터
        elif center_type == 2:
            if metadata['ct'][2] == 0:
                dispatcher.utter_message(
                    center_description[8])
            elif metadata['ct'][2] == 1:
                dispatcher.utter_message(
                    center_description[9])
        # 감정센터
        elif center_type == 3:
            if metadata['ct'][3] == 0:
                dispatcher.utter_message(
                    center_description[10])
            elif metadata['ct'][3] == 1:
                dispatcher.utter_message(
                    center_description[11])
        # 에고센터
        elif center_type == 4:
            if metadata['ct'][4] == 0:
                dispatcher.utter_message(
                    center_description[12])
            elif metadata['ct'][4] == 1:
                dispatcher.utter_message(
                    center_description[13])
        # 방향센터
        elif center_type == 5:
            if metadata['ct'][5] == 0:
                dispatcher.utter_message(
                    center_description[14])
            elif metadata['ct'][5] == 1:
                dispatcher.utter_message(
                    center_description[15])

        # 표현센터
        elif center_type == 6:
            if metadata['ct'][6] == 0:
                dispatcher.utter_message(
                    center_description[16])
            elif metadata['ct'][6] == 1:
                dispatcher.utter_message(
                    center_description[17])
        # 생각센터
        elif center_type == 7:
            if metadata['ct'][7] == 0:
                dispatcher.utter_message(
                    center_description[18])
            elif metadata['ct'][7] == 1:
                dispatcher.utter_message(
                    center_description[19])
        # 영감센터
        elif center_type == 8:
            if metadata['ct'][8] == 0:
                dispatcher.utter_message(
                    center_description[20])
            elif metadata['ct'][8] == 1:
                dispatcher.utter_message(
                    center_description[21])

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
            center_name = "연료센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/root.png"
            msg = center_description[22]
            msg2 = center_description[23]
            msg3 = center_description[24]
            msg4 = center_description[25]
        elif h_center == 1 and metadata["ct"][1] == 1:
            h_type = "활력 센터 ( 정의 )"
            center_name = "활력센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/sacral.png"
            msg = center_description[29]
            msg2 = center_description[30]
        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            center_name = "직관센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/spleen.png"
            msg = center_description[31]
            msg2 = center_description[32]
            msg3 = center_description[33]
            msg4 = center_description[34]

        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            center_name = "감정센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/solar.png"
            msg = center_description[40]
            msg2 = center_description[41]
            msg3 = center_description[42]
            msg4 = center_description[43]

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            center_name = "에고센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/heart.png"
            msg = center_description[49]
            msg2 = center_description[50]

        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            center_name = "방향센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/g.png"
            msg = center_description[56]
            msg2 = center_description[57]
            msg3 = center_description[58]
            msg4 = center_description[59]


        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            center_name = "표현센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/throat.png"
            msg = center_description[66]
            msg2 = center_description[67]
            msg3 = center_description[68]
            msg4 = center_description[69]
        elif h_center == 7 and metadata["ct"][7] == 1:
            h_type = "생각 센터 ( 정의 )"
            center_name = "생각센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/ajna.png"
            msg = center_description[75]
            msg2 = center_description[76]
        elif h_center == 8 and metadata["ct"][8] == 1:
            h_type = "영감 센터 ( 정의 )"
            center_name = "영감센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8.gif"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/head.png"
            msg = center_description[77]
            msg2 = center_description[78]
        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            center_name = "연료센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/root.png"
            msg = center_description[79]
            msg2 = center_description[80]
            msg3 = center_description[81]
            msg4 = center_description[82]
            msg5 = center_description[83]
        elif h_center == 1 and metadata['ct'][1] == 0:
            h_type = "활력 센터 ( 미정의 )"
            center_name = "활력센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_1_off.png"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/sacral_off.png"
            msg = center_description[89]
            msg2 = center_description[90]
            msg3 = center_description[91]
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            center_name = "센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/spleen_off.png"
            msg = center_description[92]
            msg2 = center_description[93]
            msg3 = center_description[94]
            msg4 = center_description[95]
            msg5 = center_description[96]

        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            center_name = "감정센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/solar_off.png"
            msg = center_description[101]
            msg2 = center_description[102]
            msg3 = center_description[103]
            msg4 = center_description[104]

        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            center_name = "에고센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/heart_off.png"
            msg = center_description[110]
            msg2 = center_description[111]
            msg3 = center_description[112]


        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            center_name = "방향센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/g_off.png"
            msg = center_description[119]
            msg2 = center_description[120]
            msg3 = center_description[121]

        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            center_name = "표현센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            img = " https://asset.i-manual.co.kr/static/images/chat/center/throat_off.png"
            msg = center_description[126]
            msg2 = center_description[127]
        elif h_center == 7 and metadata['ct'][7] == 0:
            h_type = "생각 센터 ( 미정의 )"
            center_name = "생각센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_7_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/ajna_off.png"
            msg = center_description[131]
            msg2 = center_description[132]
            msg3 = center_description[133]
        elif h_center == 8 and metadata['ct'][8] == 0:
            h_type = "영감 센터 ( 미정의 )"
            center_name = "영감센터"
            # img = "https://asset.i-manual.co.kr/static/images/centerCard/card_8_off.png"
            img = "https://asset.i-manual.co.kr/static/images/chat/center/head_off.png"
            msg = center_description[134]
            msg2 = center_description[135]

        dispatcher.utter_message(image=img)
        if msg != "":
            dispatcher.utter_message(msg)
        if msg2 != "":
            dispatcher.utter_message(msg2)
        if msg3 != "":
            dispatcher.utter_message(msg3)
        if msg4 != "":
            dispatcher.utter_message(msg4)
        if msg5 != "":
            dispatcher.utter_message(msg5)

        if h_center == 1 or h_center == 7 or h_center == 8:
            message = center_description[136].format(center_name)
            dispatcher.utter_message(message)
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
        print("MetaData: ", metadata)

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
            center_name = "연료센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0.gif"
            msg = center_description[27]
            msg2 = center_description[28]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)


        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            center_name = "직관센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2.gif"
            msg = center_description[36]
            msg2 = center_description[37]
            msg3 = center_description[38]
            msg4 = center_description[39]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)
        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            center_name = "감정센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3.gif"
            msg = center_description[45]
            msg2 = center_description[46]
            msg3 = center_description[47]
            msg4 = center_description[48]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_긴문장/3.wav"
            })

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            center_name = "에고센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4.gif"
            msg = center_description[52]
            msg2 = center_description[53]
            msg3 = center_description[54]
            msg4 = center_description[55]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            center_name = "방향센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5.gif"
            msg = center_description[61]
            msg2 = center_description[62]
            msg3 = center_description[63]
            msg4 = center_description[64]
            msg5 = center_description[65]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)
            dispatcher.utter_message(msg5)
        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            center_name = "표현센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6.gif"
            msg = center_description[71]
            msg2 = center_description[72]
            msg3 = center_description[73]
            msg4 = center_description[74]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_긴문장/4.wav"
            })
        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            center_name = "연료센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_0_off.png"
            msg = center_description[85]
            msg2 = center_description[86]
            msg3 = center_description[87]
            msg4 = center_description[88]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)

        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            center_name = "직관센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_2_off.png"
            msg = center_description[98]
            msg2 = center_description[99]
            msg3 = center_description[100]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)


        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            center_name = "감정센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_3_off.png"
            msg = center_description[106]
            msg2 = center_description[107]
            msg3 = center_description[108]
            msg4 = center_description[109]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)
        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            center_name = "에고센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_4_off.png"
            msg = center_description[114]
            msg2 = center_description[115]
            msg3 = center_description[116]
            msg4 = center_description[117]
            msg5 = center_description[118]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)
            dispatcher.utter_message(msg5)
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            center_name = "방향센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_5_off.png"
            msg = center_description[123]
            msg2 = center_description[124]
            msg3 = center_description[125]
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)

        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            center_name = "표현센터"
            img = "https://asset.i-manual.co.kr/static/images/centerCard/card_6_off.png"
            msg = center_description[129]
            msg2 = center_description[130]

            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)

        message = center_description[136].format(center_name)
        dispatcher.utter_message(message)
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

        center_step = tracker.get_slot("center_step")
        center_priority = tracker.get_slot('center_priority')

        if center_step is None or center_priority is None:
            return [FollowupAction(name='action_set_priority_again')]

        h_center = center_priority[center_step]

        buttons = []
        buttons.append({"title": f'네. 듣고 싶어요', "payload": "/leading_centers"})
        buttons.append({"title": f'아뇨 괜찮아요', "payload": "/question_intro"})

        if h_center == 0 and metadata['ct'][0] == 1:
            h_type = "연료 센터 ( 정의 )"
            dispatcher.utter_message(center_description[26], buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 1:
            h_type = "직관 센터 ( 정의 )"
            dispatcher.utter_message(center_description[35], buttons=buttons)

        elif h_center == 3 and metadata['ct'][3] == 1:
            h_type = "감정 센터 ( 정의 )"
            dispatcher.utter_message(center_description[44], buttons=buttons)

        elif h_center == 4 and metadata['ct'][4] == 1:
            h_type = "에고 센터 ( 정의 )"
            dispatcher.utter_message(center_description[51], buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 1:
            h_type = "방향 센터 ( 정의 )"
            dispatcher.utter_message(center_description[60], buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 1:
            h_type = "표현 센터 ( 정의 )"
            dispatcher.utter_message(center_description[70], buttons=buttons)



        elif h_center == 0 and metadata['ct'][0] == 0:
            h_type = "연료 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[84], buttons=buttons)
        elif h_center == 2 and metadata['ct'][2] == 0:
            h_type = "직관 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[97], buttons=buttons)
        elif h_center == 3 and metadata['ct'][3] == 0:
            h_type = "감정 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[105], buttons=buttons)
        elif h_center == 4 and metadata['ct'][4] == 0:
            h_type = "에고 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[113], buttons=buttons)
        elif h_center == 5 and metadata['ct'][5] == 0:
            h_type = "방향 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[122], buttons=buttons)
        elif h_center == 6 and metadata['ct'][6] == 0:
            h_type = "표현 센터 ( 미정의 )"
            dispatcher.utter_message(center_description[128], buttons=buttons)

        return []
# class ActionCenterMore(Action):
#    def name(self) -> Text:
#        return "action_center_more"

#    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        print('action_center_more')
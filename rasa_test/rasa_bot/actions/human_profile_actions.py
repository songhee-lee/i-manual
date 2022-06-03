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

profile_description_csv = pd.read_csv("./data/profile_description.csv")
profile_description = profile_description_csv['paragraph'].values.tolist()

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = etc_description_csv['paragraph'].values.tolist()

class ActionLeadingProfileIntro(Action):
    def name(self) -> Text:
        return "action_leading_profile_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_profile_intro')

        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        is_finished = tracker.get_slot('is_finished')

        if leading_priority is None or step is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]

        if is_finished == 1:
            dispatcher.utter_message(
                profile_description[0]
            )

        if (metadata["p"] == 13):
            dispatcher.utter_message(
                profile_description[1])
        elif (metadata["p"] == 14):
            dispatcher.utter_message(
                profile_description[2])
        elif (metadata["p"] == 24):
            dispatcher.utter_message(
                profile_description[3], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/30401.wav"
        })
        elif (metadata["p"] == 25):
            dispatcher.utter_message(
                profile_description[4])
        elif (metadata["p"] == 35):
            dispatcher.utter_message(
                profile_description[5])
        elif (metadata["p"] == 36):
            dispatcher.utter_message(
                profile_description[6])
        elif (metadata["p"] == 41):
            dispatcher.utter_message(
                profile_description[7])
        elif (metadata["p"] == 46):
            dispatcher.utter_message(
                profile_description[8])
        elif (metadata["p"] == 51):
            dispatcher.utter_message(
                profile_description[9])
        elif (metadata["p"] == 52):
            dispatcher.utter_message(
                profile_description[10])
        elif (metadata["p"] == 62):
            dispatcher.utter_message(
                profile_description[11])
        elif (metadata["p"] == 63):
            dispatcher.utter_message(
                profile_description[12])

        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        msg6 = ""
        msg7 = ""
        if metadata["p"] == 13:
            h_type = "1/3"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/13.gif"
            msg = profile_description[13]
            msg2 = profile_description[14]
            msg3 = profile_description[15]
            msg4 = profile_description[16]
            msg5 = profile_description[17]
            msg6 = profile_description[18]
            tag = "원리원칙 지킴이,내성적인 타입,실패를 두려워 말 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 14:
            h_type = "1/4"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/14.gif"
            msg = profile_description[21]
            msg2 = profile_description[22]
            msg3 = profile_description[23]
            msg4 = profile_description[24]
            tag = "원리원칙 지킴이,메신저 역할,모임에 많이 나갈 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 24:
            h_type = "2/4"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/24.gif"
            msg = profile_description[27]
            msg2 = profile_description[28]
            msg3 = profile_description[29]
            tag = "숨길 수 없는 재능,관심 신경 안씀,내 팀을 구상할 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(msg, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/32801.wav"
                })
            if msg2 != "":
                dispatcher.utter_message(msg2, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/32901.wav"
                })
            if msg3 != "":
                dispatcher.utter_message(msg3, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33001.wav"
                })

        elif metadata["p"] == 25:
            h_type = "2/5"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/25.gif"
            msg = profile_description[35]
            msg2 = profile_description[36]
            msg3 = profile_description[37]
            msg4 = profile_description[38]
            msg5 = profile_description[39]
            msg6 = profile_description[40]
            tag = "기대를 한몸에 ,혼자가 편해요 ,츤데레 컨셉 유지할 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 35:
            h_type = "3/5"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/35.gif"
            msg = profile_description[41]
            msg2 = profile_description[42]
            msg3 = profile_description[43]
            tag = "의심이 많음 ,시행착오는 나의 힘 ,꼬리를 무는 생각은 그만"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 36:
            h_type = "3/6"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/36.gif"
            msg = profile_description[48]
            msg2 = profile_description[49]
            msg3 = profile_description[50]
            tag = "아프니까 청춘이다,인생은 3막부터 ,고비를 기회로 생각할 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 41:
            h_type = "4/1"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/41.gif"
            msg = profile_description[54]
            msg2 = profile_description[55]
            msg3 = profile_description[56]
            msg4 = profile_description[57]
            msg5 = profile_description[58]
            msg6 = profile_description[59]
            msg7 = profile_description[60]
            tag = "안정감 추구 ,끝없는 연구,고집은 잠시 내려놓을 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 46:
            h_type = "4/6"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/46.gif"
            msg = profile_description[61]
            msg2 = profile_description[62]
            msg3 = profile_description[63]
            tag = "기회는 인맥에서 ,친근함이 무기 ,언행일치로 신뢰를 얻을 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 51:
            h_type = "5/1"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/51.gif"
            msg = profile_description[67]
            msg2 = profile_description[68]
            msg3 = profile_description[69]
            msg4 = profile_description[70]
            msg5 = profile_description[71]
            tag = "준비된 해결사,위기의 영웅 ,새로운 정보를 흡수할 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 52:
            h_type = "5/2"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/52.gif"
            msg = profile_description[72]
            msg2 = profile_description[73]
            msg3 = profile_description[74]
            msg4 = profile_description[75]
            msg5 = profile_description[76]
            msg6 = profile_description[77]
            msg7 = profile_description[78]
            tag = "동기부여가 중요해 ,부담되는 기대감 ,적재적소에 해결사가 될 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 62:
            h_type = "6/2"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/62.gif"
            msg = profile_description[83]
            msg2 = profile_description[84]
            msg3 = profile_description[85]
            msg4 = profile_description[86]
            tag = "방해 극혐 ,혼자가 더 재밌어 ,인파에서 벗어나 휴식할 것"
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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 63:
            h_type = "6/3"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/63.gif"
            msg = profile_description[89]
            msg2 = profile_description[90]
            msg3 = profile_description[91]
            msg4 = profile_description[92]
            msg5 = profile_description[93]
            msg6 = profile_description[94]
            tag = "몸으로 부딪히기 ,경험으로 인한 성장,주변에 소홀하지 말 것"

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
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)

        if leading_priority[0] == 1:
            step = 1
        elif leading_priority[1] == 1:
            step = 2
        elif leading_priority[2] == 1:
            step = 3
        elif leading_priority[3] == 1:
            step = 4

        if metadata["p"] == 25 or metadata["p"] == 41 or metadata["p"] == 51 or metadata["p"] == 63:
            message = profile_description[96].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
            })
            return [SlotSet('step', step), FollowupAction(name='action_question_intro')]

        buttons = []
        buttons.append({"title": f'예', "payload": "/leading_profile"})
        buttons.append({"title": f'아니요', "payload": "/question_intro"})
        dispatcher.utter_message(profile_description[95], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/39601.wav"
        })

        dispatcher.utter_message(buttons=buttons)
        # 마지막 센터에 밑에 주석 제거
        return [SlotSet('step', step)]



class ActionLeadingProfile(Action):
    def name(self) -> Text:
        return "action_leading_profile"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_profile')

        metadata = extract_metadata_from_tracker(tracker)

        # msg4 = "그러나 이러한 원리와 원칙을 기반으로 많은 시도를 통해 잘 준비되어졌을 때, 매우 강해집니다. 당신은 자기자신이 단단하게 무르익어가는 과정에 몰입하며 그 결과로 자신이 강해지거나 자신에게 힘이 되는 것을 찾아내게 될 것입니다."
        # msg5 = "변화에 대한 적응력과 엄청난 회복력을 지닌 당신은, 시행착오로 쓰러진 자신을 오뚝이처럼 다시 일으켜 세워 세상을 향해 무엇이 ‘잘못된 것’인지를 발견하고 보여줍니다. 원리와 원칙을 잘 갖추고, 시행착오를 겪는 것에 좌절하거나 무기력해지지 않고 꿋꿋이 나아가는 것이야말로 진정 당신이 타고난 모습입니다. "
        # tag = "원리원칙 지킴이,내성적인 타입,실패를 두려워 말 것"
        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        if leading_priority is None or step is None:
            return [FollowupAction(name='action_set_priority_again')]
        msg4 = ""
        msg5 = ""
        msg6 = ""
        msg7 = ""
        msg8 = ""
        h_type = ''
        if metadata["p"] == 13:
            h_type = "1/3"
            msg4 = profile_description[19]
            msg5 = profile_description[20]
            tag = "원리원칙 지킴이,내성적인 타입,실패를 두려워 말 것"
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 14:
            h_type = "1/4"
            msg4 = profile_description[25]
            msg5 = profile_description[26]
            tag = "원리원칙 지킴이,메신저 역할,모임에 많이 나갈 것"
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 24:
            h_type = "2/4"
            msg4 = profile_description[30]
            msg5 = profile_description[31]
            msg6 = profile_description[32]
            msg7 = profile_description[33]
            msg8 = profile_description[34]
            tag = "숨길 수 없는 재능,관심 신경 안씀,내 팀을 구상할 것"
            if msg4 != "":
                dispatcher.utter_message(msg4, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33101.wav"
                })
            if msg5 != "":
                dispatcher.utter_message(msg5, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33201.wav"
                })
            if msg6 != "":
                dispatcher.utter_message(msg6, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33301.wav"
                })
            if msg7 != "":
                dispatcher.utter_message(msg7, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33401.wav"
                })
            #if msg8 != "":
            #    dispatcher.utter_message(msg7, json_message={
            #        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33501.wav"
            #    })
        elif metadata["p"] == 35:
            h_type = "3/5"
            msg4 = profile_description[44]
            msg5 = profile_description[45]
            msg6 = profile_description[46]
            msg7 = profile_description[47]
            tag = "의심이 많음 ,시행착오는 나의 힘 ,꼬리를 무는 생각은 그만"
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 36:
            h_type = "3/6"
            msg4 = profile_description[51]
            msg5 = profile_description[52]
            msg6 = profile_description[53]
            tag = "아프니까 청춘이다,인생은 3막부터 ,고비를 기회로 생각할 것"
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 46:
            h_type = "4/6"
            msg4 = profile_description[64]
            msg5 = profile_description[65]
            msg6 = profile_description[66]
            tag = "기회는 인맥에서 ,친근함이 무기 ,언행일치로 신뢰를 얻을 것"
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 52:
            h_type = "5/2"
            msg4 = profile_description[79]
            msg5 = profile_description[80]
            msg6 = profile_description[81]
            msg7 = profile_description[82]

            tag = "동기부여가 중요해 ,부담되는 기대감 ,적재적소에 해결사가 될 것"
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
        elif metadata["p"] == 62:
            h_type = "6/2"
            msg4 = profile_description[87]
            msg5 = profile_description[88]
            tag = "방해 극혐 ,혼자가 더 재밌어 ,인파에서 벗어나 휴식할 것"

            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)

        dispatcher.utter_message(f"자, {h_type} 역할에 대해 설명해 보았어요.", json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33501.wav"
        })
        buttons = []
        buttons.append({"title": f'질문 있어요', "payload": "/question{\"is_question\":\"1\", \"center_question\":\"0\"}"})
        buttons.append({"title": f'질문 없어요', "payload": "/leading_more"})
        dispatcher.utter_message(etc_description[4], json_message={
            "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/10501.wav"
        })
        dispatcher.utter_message(buttons=buttons)


        if leading_priority[0] == 1:
            return [SlotSet('step', 1)]
        elif leading_priority[1] == 1:
            return [SlotSet('step', 2)]
        elif leading_priority[2] == 1:
            return [SlotSet('step', 3)]
        elif leading_priority[3] == 1:
            return [SlotSet('step', 4)]
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
profile_description = []
profile_description.append(profile_description_csv['korean'].values.tolist())
profile_description.append(profile_description_csv['english'].values.tolist())
profile_description.append(profile_description_csv['voiceID'].values.tolist())

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = []
etc_description.append(etc_description_csv['korean'].values.tolist())
etc_description.append(etc_description_csv['english'].values.tolist())
etc_description.append(etc_description_csv['voiceID'].values.tolist())


class ActionLeadingProfileIntro(Action):
    def name(self) -> Text:
        return "action_leading_profile_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_profile_intro')

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
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][0])),
                "data": profile_description[lang][0]
            })

        if (metadata["p"] == 13):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][1])),
                "data": profile_description[lang][1]
            })
        elif (metadata["p"] == 14):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][2])),
                "data": profile_description[lang][2]
            })
        elif (metadata["p"] == 24):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][3])),
                "data": profile_description[lang][3]
            })
        elif (metadata["p"] == 25):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][4])),
                "data": profile_description[lang][4]
            })
        elif (metadata["p"] == 35):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][5])),
                "data": profile_description[lang][5]
            })
        elif (metadata["p"] == 36):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][6])),
                "data": profile_description[lang][6]
            })
        elif (metadata["p"] == 41):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][7])),
                "data": profile_description[lang][7]
            })
        elif (metadata["p"] == 46):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][8])),
                "data": profile_description[lang][8]
            })
        elif (metadata["p"] == 51):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][9])),
                "data": profile_description[lang][9]
            })
        elif (metadata["p"] == 52):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][10])),
                "data": profile_description[lang][10]
            })
        elif (metadata["p"] == 62):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][11])),
                "data": profile_description[lang][11]
            })
        elif (metadata["p"] == 63):
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][12])),
                "data": profile_description[lang][12]
            })

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
            msg = profile_description[lang][13]
            vID = profile_description[voice_num][13]
            msg2 = profile_description[lang][14]
            vID2 = profile_description[voice_num][14]
            msg3 = profile_description[lang][15]
            vID3 = profile_description[voice_num][15]
            msg4 = profile_description[lang][16]
            vID4 = profile_description[voice_num][16]
            msg5 = profile_description[lang][17]
            vID5 = profile_description[voice_num][17]
            msg6 = profile_description[lang][18]
            vID6 = profile_description[voice_num][18]
            tag = "원리원칙 지킴이,내성적인 타입,실패를 두려워 말 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            '''
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
        elif metadata["p"] == 14:
            h_type = "1/4"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/14.gif"
            msg = profile_description[lang][21]
            vID = profile_description[voice_num][21]
            msg2 = profile_description[lang][22]
            vID2 = profile_description[voice_num][22]
            msg3 = profile_description[lang][23]
            vID3 = profile_description[voice_num][23]
            msg4 = profile_description[lang][24]
            vID4 = profile_description[voice_num][24]
            tag = "원리원칙 지킴이,메신저 역할,모임에 많이 나갈 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            '''
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
        elif metadata["p"] == 24:
            h_type = "2/4"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/24.gif"
            msg = profile_description[lang][27]
            vID = profile_description[voice_num][27]
            msg2 = profile_description[lang][28]
            vID2 = profile_description[voice_num][28]
            msg3 = profile_description[lang][29]
            vID3 = profile_description[voice_num][29]
            tag = "숨길 수 없는 재능,관심 신경 안씀,내 팀을 구상할 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })

        elif metadata["p"] == 25:
            h_type = "2/5"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/25.gif"
            msg = profile_description[lang][35]
            vID = profile_description[voice_num][35]
            msg2 = profile_description[lang][36]
            vID2 = profile_description[voice_num][36]
            msg3 = profile_description[lang][37]
            vID3 = profile_description[voice_num][37]
            msg4 = profile_description[lang][38]
            vID4 = profile_description[voice_num][38]
            msg5 = profile_description[lang][39]
            vID5 = profile_description[voice_num][39]
            msg6 = profile_description[lang][40]
            vID6 = profile_description[voice_num][40]
            tag = "기대를 한몸에 ,혼자가 편해요 ,츤데레 컨셉 유지할 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            '''
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
            message = profile_description[lang][100]
            vID = profile_description[voice_num][100]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                "data": message
            })
        elif metadata["p"] == 35:
            h_type = "3/5"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/35.gif"
            msg = profile_description[lang][41]
            vID = profile_description[voice_num][41]
            msg2 = profile_description[lang][42]
            vID2 = profile_description[voice_num][42]
            msg3 = profile_description[lang][43]
            vID3 = profile_description[voice_num][43]
            tag = "의심이 많음 ,시행착오는 나의 힘 ,꼬리를 무는 생각은 그만"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            '''
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
        elif metadata["p"] == 36:
            h_type = "3/6"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/36.gif"
            msg = profile_description[lang][48]
            vID = profile_description[voice_num][48]
            msg2 = profile_description[lang][49]
            vID2 = profile_description[voice_num][49]
            msg3 = profile_description[lang][50]
            vID3 = profile_description[voice_num][50]
            tag = "아프니까 청춘이다,인생은 3막부터 ,고비를 기회로 생각할 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            '''
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
        elif metadata["p"] == 41:
            h_type = "4/1"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/41.gif"
            msg = profile_description[lang][54]
            vID = profile_description[voice_num][54]
            msg2 = profile_description[lang][55]
            vID2 = profile_description[voice_num][55]
            msg3 = profile_description[lang][56]
            vID3 = profile_description[voice_num][56]
            msg4 = profile_description[lang][57]
            vID4 = profile_description[voice_num][57]
            msg5 = profile_description[lang][58]
            vID5 = profile_description[voice_num][58]
            msg6 = profile_description[lang][59]
            vID6 = profile_description[voice_num][59]
            msg7 = profile_description[lang][60]
            vID7 = profile_description[voice_num][60]
            tag = "안정감 추구 ,끝없는 연구,고집은 잠시 내려놓을 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID7)),
                    "data": msg7
                })
            message = profile_description[lang][103]
            vID = profile_description[voice_num][103]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                "data": message
            })
        elif metadata["p"] == 46:
            h_type = "4/6"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/46.gif"
            msg = profile_description[lang][61]
            vID = profile_description[voice_num][61]
            msg2 = profile_description[lang][62]
            vID2 = profile_description[voice_num][62]
            msg3 = profile_description[lang][63]
            vID3 = profile_description[voice_num][63]
            tag = "기회는 인맥에서 ,친근함이 무기 ,언행일치로 신뢰를 얻을 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            '''

            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
        elif metadata["p"] == 51:
            h_type = "5/1"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/51.gif"
            msg = profile_description[lang][67]
            vID = profile_description[voice_num][67]
            msg2 = profile_description[lang][68]
            vID2 = profile_description[voice_num][68]
            msg3 = profile_description[lang][69]
            vID3 = profile_description[voice_num][69]
            msg4 = profile_description[lang][70]
            vID4 = profile_description[voice_num][70]
            msg5 = profile_description[lang][71]
            vID5 = profile_description[voice_num][71]
            tag = "준비된 해결사,위기의 영웅 ,새로운 정보를 흡수할 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            '''
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
            message = profile_description[lang][105]
            vID = profile_description[voice_num][105]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                "data": message
            })
        elif metadata["p"] == 52:
            h_type = "5/2"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/52.gif"
            msg = profile_description[lang][72]
            vID = profile_description[voice_num][72]
            msg2 = profile_description[lang][73]
            vID2 = profile_description[voice_num][73]
            msg3 = profile_description[lang][74]
            vID3 = profile_description[voice_num][74]
            msg4 = profile_description[lang][75]
            vID4 = profile_description[voice_num][75]
            msg5 = profile_description[lang][76]
            vID5 = profile_description[voice_num][76]
            msg6 = profile_description[lang][77]
            vID6 = profile_description[voice_num][77]
            msg7 = profile_description[lang][78]
            vID7 = profile_description[voice_num][78]
            tag = "동기부여가 중요해 ,부담되는 기대감 ,적재적소에 해결사가 될 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID7)),
                    "data": msg7
                })
        elif metadata["p"] == 62:
            h_type = "6/2"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/62.gif"
            msg = profile_description[lang][83]
            vID = profile_description[voice_num][83]
            msg2 = profile_description[lang][84]
            vID2 = profile_description[voice_num][84]
            msg3 = profile_description[lang][85]
            vID3 = profile_description[voice_num][85]
            msg4 = profile_description[lang][86]
            vID4 = profile_description[voice_num][86]
            tag = "방해 극혐 ,혼자가 더 재밌어 ,인파에서 벗어나 휴식할 것"
            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            '''
            if msg5 != "":
                dispatcher.utter_message(msg5)
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
        elif metadata["p"] == 63:
            h_type = "6/3"
            img = "https://asset.i-manual.co.kr/static/images/profile/profiles/63.gif"
            msg = profile_description[lang][89]
            vID = profile_description[voice_num][89]
            msg2 = profile_description[lang][90]
            vID2 = profile_description[voice_num][90]
            msg3 = profile_description[lang][91]
            vID3 = profile_description[voice_num][91]
            msg4 = profile_description[lang][92]
            vID4 = profile_description[voice_num][92]
            msg5 = profile_description[lang][93]
            vID5 = profile_description[voice_num][93]
            msg6 = profile_description[lang][94]
            vID6 = profile_description[voice_num][94]
            tag = "몸으로 부딪히기 ,경험으로 인한 성장,주변에 소홀하지 말 것"

            dispatcher.utter_message(image=img)

            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                    "data": msg
                })
            if msg2 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID2)),
                    "data": msg2
                })
            if msg3 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID3)),
                    "data": msg3
                })
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            '''
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
            message = profile_description[lang][108]
            vID = profile_description[voice_num][108]
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                "data": message
            })

        if leading_priority[0] == 1:
            step = 1
        elif leading_priority[1] == 1:
            step = 2
        elif leading_priority[2] == 1:
            step = 3
        elif leading_priority[3] == 1:
            step = 4

        if metadata["p"] == 25 or metadata["p"] == 41 or metadata["p"] == 51 or metadata["p"] == 63:
            # message = profile_description[lang][96].format(h_type)
            # vID = profile_description[voice_num][96]
            # dispatcher.utter_message(json_message={
            #     "type": "voiceID", "sender": metadata['uID'], "content": "{0}/{1}/{2}.mp3".format(lang, ninei, vID),
            #     "data": message
            # })
            return [SlotSet('step', step), FollowupAction(name='action_question_intro')]

        buttons = []
        buttons.append({"title": etc_description[lang][23], "payload": "/leading_profile"})  # 예
        buttons.append({"title": etc_description[lang][24], "payload": "/question_intro"})  # 아니오
        dispatcher.utter_message(json_message={
            "type": "voiceID", "sender": metadata['uID'],
            "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][95])),
            "data": profile_description[lang][95]
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
        lang = metadata['lang']
        ninei = metadata['member']

        # msg4 = "그러나 이러한 원리와 원칙을 기반으로 많은 시도를 통해 잘 준비되어졌을 때, 매우 강해집니다. 당신은 자기자신이 단단하게 무르익어가는 과정에 몰입하며 그 결과로 자신이 강해지거나 자신에게 힘이 되는 것을 찾아내게 될 것입니다."
        # msg5 = "변화에 대한 적응력과 엄청난 회복력을 지닌 당신은, 시행착오로 쓰러진 자신을 오뚝이처럼 다시 일으켜 세워 세상을 향해 무엇이 ‘잘못된 것’인지를 발견하고 보여줍니다. 원리와 원칙을 잘 갖추고, 시행착오를 겪는 것에 좌절하거나 무기력해지지 않고 꿋꿋이 나아가는 것이야말로 진정 당신이 타고난 모습입니다. "
        # tag = "원리원칙 지킴이,내성적인 타입,실패를 두려워 말 것"
        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        voice_num = tracker.get_slot('voice_num')
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
            msg4 = profile_description[lang][19]
            vID4 = profile_description[voice_num][19]
            msg5 = profile_description[lang][20]
            vID5 = profile_description[voice_num][20]
            tag = "원리원칙 지킴이,내성적인 타입,실패를 두려워 말 것"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            '''
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][97])),
                "data": profile_description[lang][97]
            })
        elif metadata["p"] == 14:
            h_type = "1/4"
            msg4 = profile_description[lang][25]
            vID4 = profile_description[voice_num][25]
            msg5 = profile_description[lang][26]
            vID5 = profile_description[voice_num][26]
            tag = "원리원칙 지킴이,메신저 역할,모임에 많이 나갈 것"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            '''
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            '''
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][98])),
                "data": profile_description[lang][98]
            })
        elif metadata["p"] == 24:
            h_type = "2/4"
            msg4 = profile_description[lang][30]
            vID4 = profile_description[voice_num][30]
            msg5 = profile_description[lang][31]
            vID5 = profile_description[voice_num][31]
            msg6 = profile_description[lang][32]
            vID6 = profile_description[voice_num][32]
            msg7 = profile_description[lang][33]
            vID7 = profile_description[voice_num][33]
            msg8 = profile_description[lang][34]
            vID8 = profile_description[voice_num][34]
            tag = "숨길 수 없는 재능,관심 신경 안씀,내 팀을 구상할 것"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID7)),
                    "data": msg7
                })
            # if msg8 != "":
            #    dispatcher.utter_message(msg7, json_message={
            #        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/33501.mp3", "data" : 
            #    })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][99])),
                "data": profile_description[lang][99]
            })
        elif metadata["p"] == 35:
            h_type = "3/5"
            msg4 = profile_description[lang][44]
            vID4 = profile_description[voice_num][44]
            msg5 = profile_description[lang][45]
            vID5 = profile_description[voice_num][45]
            msg6 = profile_description[lang][46]
            vID6 = profile_description[voice_num][46]
            msg7 = profile_description[lang][47]
            vID7 = profile_description[voice_num][47]
            tag = "의심이 많음 ,시행착오는 나의 힘 ,꼬리를 무는 생각은 그만"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID7)),
                    "data": msg7
                })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][101])),
                "data": profile_description[lang][101]
            })
        elif metadata["p"] == 36:
            h_type = "3/6"
            msg4 = profile_description[lang][51]
            vID4 = profile_description[voice_num][51]
            msg5 = profile_description[lang][52]
            vID5 = profile_description[voice_num][52]
            msg6 = profile_description[lang][53]
            vID6 = profile_description[voice_num][53]
            tag = "아프니까 청춘이다,인생은 3막부터 ,고비를 기회로 생각할 것"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(msg7)
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][102])),
                "data": profile_description[lang][102]
            })
        elif metadata["p"] == 46:
            h_type = "4/6"
            msg4 = profile_description[lang][64]
            vID4 = profile_description[voice_num][64]
            msg5 = profile_description[lang][65]
            vID5 = profile_description[voice_num][65]
            msg6 = profile_description[lang][66]
            vID6 = profile_description[voice_num][66]
            tag = "기회는 인맥에서 ,친근함이 무기 ,언행일치로 신뢰를 얻을 것"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(msg7)
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][104])),
                "data": profile_description[lang][104]
            })
        elif metadata["p"] == 52:
            h_type = "5/2"
            msg4 = profile_description[lang][79]
            vID4 = profile_description[voice_num][79]
            msg5 = profile_description[lang][80]
            vID5 = profile_description[voice_num][80]
            msg6 = profile_description[lang][81]
            vID6 = profile_description[voice_num][81]
            msg7 = profile_description[lang][82]
            vID7 = profile_description[voice_num][82]

            tag = "동기부여가 중요해 ,부담되는 기대감 ,적재적소에 해결사가 될 것"
            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID6)),
                    "data": msg6
                })
            if msg7 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID7)),
                    "data": msg7
                })
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][106])),
                "data": profile_description[lang][106]
            })
        elif metadata["p"] == 62:
            h_type = "6/2"
            msg4 = profile_description[lang][87]
            vID4 = profile_description[voice_num][87]
            msg5 = profile_description[lang][88]
            vID5 = profile_description[voice_num][88]
            tag = "방해 극혐 ,혼자가 더 재밌어 ,인파에서 벗어나 휴식할 것"

            if msg4 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID4)),
                    "data": msg4
                })
            if msg5 != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", "sender": metadata['uID'],
                    "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID5)),
                    "data": msg5
                })
            if msg6 != "":
                dispatcher.utter_message(msg6)
            if msg7 != "":
                dispatcher.utter_message(msg7)
            dispatcher.utter_message(json_message={
                "type": "voiceID", "sender": metadata['uID'],
                "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(profile_description[voice_num][107])),
                "data": profile_description[lang][107]
            })
        # dispatcher.utter_message(json_message={
        #     "type": "voiceID", "sender": metadata['uID'],
        #     "content": "{0}/{1}/{2}.mp3".format(lang, ninei, profile_description[voice_num][96]),
        #     "data": profile_description[lang][96].format(h_type)
        # })


        buttons = []
        buttons.append({"title": etc_description[lang][18],
                        "payload": "/question{\"is_question\":\"1\", \"center_question\":\"0\"}"})  # 질문 있어요
        buttons.append({"title": etc_description[lang][19], "payload": "/leading_more"})  # 질문 없어요
        dispatcher.utter_message(json_message={
            "type": "voiceID", "sender": metadata['uID'],
            "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(etc_description[voice_num][4])),
            "data": etc_description[lang][4]
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

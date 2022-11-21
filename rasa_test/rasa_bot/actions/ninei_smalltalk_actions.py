import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker
from rasa_sdk.events import FollowupAction
import pandas as pd
from actions.common import get_TTS

logger = logging.getLogger(__name__)

smalltalk_question_csv = pd.read_csv("./data/smalltalk_question.csv")
smalltalk_question = []
smalltalk_question.append(smalltalk_question_csv['korean'].values.tolist())
smalltalk_question.append(smalltalk_question_csv['english'].values.tolist())
smalltalk_question.append(smalltalk_question_csv['voiceID'].values.tolist())

smalltalk_answer_csv = pd.read_csv("./data/smalltalk_answer.csv")
smalltalk_answer = []
smalltalk_answer.append(smalltalk_answer_csv['korean'].values.tolist())
smalltalk_answer.append(smalltalk_answer_csv['english'].values.tolist())

ninei_members = [['', '민준', '반', '베리', '서원', '위니', '이든', '제원', '주형', '지호', '태훈'],
                 ['', 'MIN JUN', 'VAHN', 'VARI', 'SEO WON', 'WINNIE', 'EDEN', 'JE WON', 'JOO HYOUNG', 'JI HO',
                  'TAE HUN']]


class ActionSmalltalkFirst(Action):
    def name(self) -> Text:
        return "action_smalltalk_first"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_smalltalk_first')

        metadata = extract_metadata_from_tracker(tracker)
        smalltalk_step = tracker.get_slot('smalltalk_step')
        ninei = metadata['member']
        lang = metadata['lang']
        voice_num = tracker.get_slot('voice_num')
        question = smalltalk_question[lang][smalltalk_step].format(metadata['pn'], ninei_members[lang][ninei])
        is_real_time = False
        if smalltalk_step in [2, 3, 9, 10, 21, 22, 25, 29, 32, 33, 34, 35, 37, 38, 43, 44]: # 실시간 생성하는 경우
            vID = get_TTS(question, metadata) #생성하고 경로를 가져옴 /// get_TTS의 함수를 고객 이름 + vid로 해야 겠음
            dispatcher.utter_message(json_message={
                        "type": "voiceID", "sender": metadata['uID'], "content": vID,
                        "data": question
                    })
        else:
            vID = smalltalk_question[voice_num][smalltalk_step]
            dispatcher.utter_message(json_message={
                        "type": "voiceID", "sender": metadata['uID'], 
                        "content": "{0}/{1}/{2}.mp3".format(lang, ninei, int(vID)),
                        "data": question
                    })
        # buttons 요소 2개 이상
        if smalltalk_step in [3, 22, 25, 35, 38]:
            buttons = []
            if smalltalk_step == 3:
                
                buttons.append(
                    {"title": smalltalk_answer[lang][3], "payload": "/change_smalltalk_step{\"smalltalk_step\":3}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][4], "payload": "/change_smalltalk_step{\"smalltalk_step\":4}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][5], "payload": "/change_smalltalk_step{\"smalltalk_step\":5}"}
                )
            elif smalltalk_step == 22:
                
                buttons.append(
                    {"title": smalltalk_answer[lang][22], "payload": "/change_smalltalk_step{\"smalltalk_step\":24}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][23], "payload": "/change_smalltalk_step{\"smalltalk_step\":24}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][24], "payload": "/change_smalltalk_step{\"smalltalk_step\":24}"}
                )
            elif smalltalk_step == 25:
                
                buttons.append(
                    {"title": smalltalk_answer[lang][25], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][26], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][27], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][28], "payload": "/change_smalltalk_step{\"smalltalk_step\":28}"}
                )
            elif smalltalk_step == 35:
                
                buttons.append(
                    {"title": smalltalk_answer[lang][35], "payload": "/change_smalltalk_step{\"smalltalk_step\":36}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][36], "payload": "/change_smalltalk_step{\"smalltalk_step\":36}"}
                )
            elif smalltalk_step == 38:
                
                
                buttons.append(
                    {"title": smalltalk_answer[lang][38], "payload": "/change_smalltalk_step{\"smalltalk_step\":38}"}
                )
                buttons.append(
                    {"title": smalltalk_answer[lang][39], "payload": "/change_smalltalk_step{\"smalltalk_step\":39}"}
                )

            dispatcher.utter_message(buttons=buttons)

        # buttons 요소 없음
        elif smalltalk_step in [31, 33, 41, 42, 44, 45]:

            return [FollowupAction(name="action_change_smalltalk_step")]

        # buttons 요소 1개
        else:
            buttons = [{"title": smalltalk_answer[lang][smalltalk_step],
                        "payload": "/change_smalltalk_step"}]

            dispatcher.utter_message(buttons=buttons)


class ActionChangeSmalltalkStep(Action):
    def name(self) -> Text:
        return "action_change_smalltalk_step"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('action_change_smalltalk_step')

        smalltalk_step = tracker.get_slot('smalltalk_step')
        disappointed = tracker.get_slot('disappointed')
        

        # 첫인사 끝
        if smalltalk_step in [34]:  # 종료
            return [FollowupAction(name="action_start"), ]
        if smalltalk_step == 37:  # 재방문 인사 끝
            return [FollowupAction(name="action_masterbot"), SlotSet("regreetings", 1)]
        if smalltalk_step == 45:
            return []  # 마무리 인사 끝
        if smalltalk_step == 40:
            return [SlotSet("smalltalk_step", smalltalk_step + 3), FollowupAction(name="action_smalltalk_first")]
        if smalltalk_step == 41:  # 실망한 경우, 슬롯 값 변경후 대기, 입력값을 받고 ActionDefaultFallback 실행
            return [SlotSet("disappointed", 1)]
        if smalltalk_step in range(38, 40):
            return [SlotSet("smalltalk_step", smalltalk_step + 2), FollowupAction(name="action_smalltalk_first")]
        if smalltalk_step in range(3, 6):
            return [SlotSet("smalltalk_step", smalltalk_step + 3), FollowupAction(name="action_smalltalk_first")]
        elif smalltalk_step in range(6, 8):
            return [SlotSet("smalltalk_step", 10), FollowupAction(name="action_smalltalk_first")]
        elif smalltalk_step == 10:  # 나인아이 멤버 자기소개 단계일 때
            metadata = extract_metadata_from_tracker(tracker)
            ninei = metadata['member']
            if metadata["lang"] == 0:
                img = "https://webapp-dev.i-manual.co.kr/static/images/chat/ninei/profile/ko/{0}.png".format(ninei)
                dispatcher.utter_message(image=img)
            else:
                img = "https://webapp-dev.i-manual.co.kr/static/images/chat/ninei/profile/en/{0}.png".format(ninei)
                dispatcher.utter_message(image=img)
            return [SlotSet("smalltalk_step", smalltalk_step + ninei), FollowupAction(name="action_smalltalk_first")]
        elif smalltalk_step in range(11, 21):
            return [SlotSet("smalltalk_step", 21), FollowupAction(name="action_smalltalk_first")]

        return [SlotSet("smalltalk_step", smalltalk_step + 1), FollowupAction(name="action_smalltalk_first")]
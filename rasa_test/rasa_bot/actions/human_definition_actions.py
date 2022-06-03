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
definition_description = definition_description_csv['paragraph'].values.tolist()


class ActionLeadingDefinitionIntro(Action):
    def name(self) -> Text:
        return "action_leading_definition_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_definition_intro')

        metadata = extract_metadata_from_tracker(tracker)
        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        is_finished = tracker.get_slot('is_finished')

        if leading_priority is None or step is None or is_finished is None:
            return [FollowupAction(name='action_set_priority_again')]

        if is_finished == 1:
            dispatcher.utter_message(
                definition_description[0]
            )

        if (metadata["d"] == 0):
            dispatcher.utter_message(
                f'절전모드 인트로')
        elif (metadata["d"] == 1):
            dispatcher.utter_message(
                definition_description[1])
        elif (metadata["d"] == 2):
            dispatcher.utter_message(
                definition_description[2])
        elif (metadata["d"] == 3):
            dispatcher.utter_message(
                definition_description[3], json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/40401.wav"
                })
        elif (metadata["d"] == 4):
            dispatcher.utter_message(
                definition_description[4])

        msg = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        msg5 = ""
        h_type = ''
        if metadata["d"] == 0:
            h_type = "절전모드"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_0.png"
            # msg = "절전모드 간단한 설명입니다."
            # msg2 = "앞 부분 설명"
            msg3 = "나와 함께 있는 다른 사람의 에너지, 혹은 오늘의 나를 통해 나에게 연결되는 에너지처럼 외부 요인에 의해 크게 영향을 받습니다. 활발한 사람과 있을 때에는 힘이 넘쳐 신나게 움직이고 놀고 활동적이다가도, 그 사람과의 연결이 끊어져 혼자 남으면 고요한 상태, 그야말로 잠잠한 절전모드가 됩니다."
            msg4 = "꼭 사람과의 연결이 아니어도 오늘 내가 연결되는 에너지가 무엇이냐에 따라 하루 종일 활발할 수도 있습니다.당신이 어떤 활발한 에너지에 연결되었을 때 그 영향으로 너무 무리하는 것보다는 적절하게 틈틈히 휴식을 챙기는게 더 건강에 도움이 될 수 있습니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 1% 분포에 해당됩니다."
            tag = "카멜레온,무한한 잠재성,틈틈이 휴식할 것"
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(msg, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg2 != "":
                dispatcher.utter_message(msg2, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg3 != "":
                dispatcher.utter_message(msg3, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            message = definition_description[21].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
            })
        elif metadata["d"] == 1:
            h_type = "한 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_1.png"
            msg = definition_description[5]
            msg2 = definition_description[6]
            msg3 = definition_description[7]
            msg4 = definition_description[8]
            msg5 = definition_description[9]
            tag = "혼자서도 잘해요,조용하면 집중력 UP,홀로 공부할 것"
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(msg, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg2 != "":
                dispatcher.utter_message(msg2, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg3 != "":
                dispatcher.utter_message(msg3, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            message = definition_description[21].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
            })
        elif metadata["d"] == 2:
            h_type = "두 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_2.png"
            msg = definition_description[10]
            msg2 = definition_description[11]
            msg3 = definition_description[12]

            tag = "카페에서도 공부 잘함,사람에 관심이 많아요,사람 많으면 아이디어 UP"
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(msg, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg2 != "":
                dispatcher.utter_message(msg2, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg3 != "":
                dispatcher.utter_message(msg3, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            message = definition_description[21].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
            })
        elif metadata["d"] == 3:
            h_type = "세 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_3.png"
            msg = definition_description[13]
            msg2 = definition_description[14]
            msg3 = definition_description[15]
            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(msg, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/41401.wav"
                })
            if msg != "":
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/41402.wav"
                })
            if msg2 != "":
                dispatcher.utter_message(msg2, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/41501.wav"
                })
                dispatcher.utter_message(json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/41502.wav"
                })
            if msg3 != "":
                dispatcher.utter_message(msg3, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/41601.wav"
                })
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)
            tag = "갈대같은 사람,한 곳에서 집중이 힘듦,자리를 바꿔 공부할 것"
            message = definition_description[21].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/42201.wav"
            })
        elif metadata["d"] == 4:
            h_type = "네 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_4.png"
            msg = definition_description[16]
            msg2 = definition_description[17]
            msg3 = definition_description[18]
            msg4 = definition_description[19]
            msg5 = definition_description[20]
            tag = "우유부단,새로운게 필요해,친구들과 공부할 것"

            dispatcher.utter_message(image=img)  # 일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
            if msg != "":
                dispatcher.utter_message(msg, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg2 != "":
                dispatcher.utter_message(msg2, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg3 != "":
                dispatcher.utter_message(msg3, json_message={
                    "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
                })
            if msg4 != "":
                dispatcher.utter_message(msg4)
            if msg5 != "":
                dispatcher.utter_message(msg5)

        # dispatcher.utter_message(json_message = {
        #                         "type": "arrContents", "content": [[msg, msg2], [msg3, msg4], [msg5]], "tags": f'{tag}'})

            message = definition_description[21].format(h_type)
            dispatcher.utter_message(message, json_message={
                "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/.wav"
            })

        if leading_priority[0] == 2:
            return [SlotSet('step', 1), FollowupAction(name='action_question_intro')]
        elif leading_priority[1] == 2:
            return [SlotSet('step', 2), FollowupAction(name='action_question_intro')]
        elif leading_priority[2] == 2:
            return [SlotSet('step', 3), FollowupAction(name='action_question_intro')]
        elif leading_priority[3] == 2:
            return [SlotSet('step', 4), FollowupAction(name='action_question_intro')]

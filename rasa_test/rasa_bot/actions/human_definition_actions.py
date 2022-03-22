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
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/1.wav"
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
            #msg = "절전모드 간단한 설명입니다."
            #msg2 = "앞 부분 설명"
            msg3 = "나와 함께 있는 다른 사람의 에너지, 혹은 오늘의 나를 통해 나에게 연결되는 에너지처럼 외부 요인에 의해 크게 영향을 받습니다. 활발한 사람과 있을 때에는 힘이 넘쳐 신나게 움직이고 놀고 활동적이다가도, 그 사람과의 연결이 끊어져 혼자 남으면 고요한 상태, 그야말로 잠잠한 절전모드가 됩니다."
            msg4 = "꼭 사람과의 연결이 아니어도 오늘 내가 연결되는 에너지가 무엇이냐에 따라 하루 종일 활발할 수도 있습니다.당신이 어떤 활발한 에너지에 연결되었을 때 그 영향으로 너무 무리하는 것보다는 적절하게 틈틈히 휴식을 챙기는게 더 건강에 도움이 될 수 있습니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 1% 분포에 해당됩니다."
            tag = "카멜레온,무한한 잠재성,틈틈이 휴식할 것"
        elif metadata["d"] == 1:
            h_type = "한 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_1.png"
            msg = definition_description[5]
            msg2 = definition_description[6]
            msg3 = definition_description[7]
            msg4 = definition_description[8]
            msg5 = definition_description[9]
            tag = "혼자서도 잘해요,조용하면 집중력 UP,홀로 공부할 것"
        elif metadata["d"] == 2:
            h_type = "두 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_2.png"
            msg = definition_description[10]
            msg2 = definition_description[11]
            msg3 = definition_description[12]
            tag = "카페에서도 공부 잘함,사람에 관심이 많아요,사람 많으면 아이디어 UP"
        elif metadata["d"] == 3:
            h_type = "세 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_3.png"
            msg = definition_description[13]
            msg2 = definition_description[14]
            msg3 = definition_description[15]
            tag = "갈대같은 사람,한 곳에서 집중이 힘듦,자리를 바꿔 공부할 것"
        elif metadata["d"] == 4:
            h_type = "네 묶음 에너지 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_4.png"
            msg = definition_description[16]
            msg2 = definition_description[17]
            msg3 = definition_description[18]
            msg4 = definition_description[19]
            msg5 = definition_description[20]
            tag = "우유부단,새로운게 필요해,친구들과 공부할 것"

        dispatcher.utter_message(image=img) #일단 나누기 전에 test용으로 json추가 했을 뿐, 실제 적용할 때는 따로 해야댐
        if msg != "":
            dispatcher.utter_message(msg, json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/2.wav"
                    })
        if msg2 != "":
            dispatcher.utter_message(msg2, json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/3.wav"
                    })
        if msg3 != "":
            dispatcher.utter_message(msg3, json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/4.wav"
                    })
        if msg4 != "":
            dispatcher.utter_message(msg4)
        if msg5 != "":
            dispatcher.utter_message(msg5)

        # dispatcher.utter_message(json_message = {
        #                         "type": "arrContents", "content": [[msg, msg2], [msg3, msg4], [msg5]], "tags": f'{tag}'})

        message = definition_description[21].format(h_type)
        dispatcher.utter_message(message, json_message={
                        "type": "voiceID", 'sender': metadata['uID'], "content": "out_5/5.wav"
                    })

        if leading_priority[0] == 2:
            return [SlotSet('step', 1), FollowupAction(name='action_question_intro')]
        elif leading_priority[1] == 2:
            return [SlotSet('step', 2), FollowupAction(name='action_question_intro')]
        elif leading_priority[2] == 2:
            return [SlotSet('step', 3), FollowupAction(name='action_question_intro')]
        elif leading_priority[3] == 2:
            return [SlotSet('step', 4), FollowupAction(name='action_question_intro')]

class ActionLeadingDefinition(Action):
    def name(self) -> Text:
        return "action_leading_definition"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_definition')

        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        if leading_priority is None or step is None:
            return [FollowupAction(name='action_set_priority_again')]
        h_type = ''
        if metadata["d"] == 0:
            h_type = "절전모드"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_0.png"
            msg = "단 하나의 에너지 흐름도 고정적으로 가지고 있지 않은 당신은 절전모드, 거울종족입니다. 거울종족은 모든 센터가 열려 있기 때문에 당신은 일관성 있게 작동하는 에너지를 하나도 가지고 있지 않습니다."
            msg2 = "일관성 있게 작동하는 에너지가 없다는 것은 때로는 활발하고 힘이 넘치고, 때로는 조용하고 잠잠하고, 정해진 기준이 없이 왔다 갔다 하는 것입니다."
            msg3 = "나와 함께 있는 다른 사람의 에너지, 혹은 오늘의 나를 통해 나에게 연결되는 에너지처럼 외부 요인에 의해 크게 영향을 받습니다. 활발한 사람과 있을 때에는 힘이 넘쳐 신나게 움직이고 놀고 활동적이다가도, 그 사람과의 연결이 끊어져 혼자 남으면 고요한 상태, 그야말로 잠잠한 절전모드가 됩니다."
            msg4 = "꼭 사람과의 연결이 아니어도 오늘 내가 연결되는 에너지가 무엇이냐에 따라 하루 종일 활발할 수도 있습니다.당신이 어떤 활발한 에너지에 연결되었을 때 그 영향으로 너무 무리하는 것보다는 적절하게 틈틈히 휴식을 챙기는게 더 건강에 도움이 될 수 있습니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 1% 분포에 해당됩니다."
            tag = "카멜레온,무한한 잠재성,틈틈이 휴식할 것"
        elif metadata["d"] == 1:
            h_type = "한 묶음 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_1.png"
            msg = "당신이 가지고 있는 에너지흐름은 다른 누구의 도움이 없이 혼자서도 잘 조화를 이루어 흐릅니다."
            msg2 = "그래서 당신은 혼자서도 자기만의 공간에서 일이나 공부에 잘 집중하여 효율적으로 해나갈 수 있고, 다른 에너지흐름을 가진 사람들보다 이해나 행동하는 데에 있어 수월합니다."
            msg3 = "혼자서도 별 문제 없이 척척 해낼 수 있는 당신은 다른 에너지와 연결하려는 필요를 느끼지 않기 때문에 외부에 그다지 관심이 없습니다. 이는 인간 관계에 대한 고민으로 이어집니다."
            msg4 = "’인간 관계란 무엇인가, 인간 관계는 어떻게 하는 것인가?’ 혼자서도 별다른 어려움이나 막힘 없이 잘 해나가는 당신이지만, 그럼에도 불구하고 그 어느 누구도 이 세상을 완전히 홀로 살아갈 수는 없기에, 사람들과 어떻게 관계하면 좋을지에 대해서는 다른 사람들로부터 지혜를 배울 수 있습니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 41% 분포에 해당됩니다."
            tag = "혼자서도 잘해요,조용하면 집중력 UP,홀로 공부할 것"
        elif metadata["d"] == 2:
            h_type = "두 묶음 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_2.png"
            msg = "혼자있을 때, 집중하여 일이나 공부가 잘 되지 않는 당신은 자신 이외의 다른 것에 대한 필요를 느끼고 있습니다."
            msg2 = "당신의 에너지들은 두 부분으로 나뉘어 흐르고 있기 때문에 혼자 자기만의 공간에서 일이나 공부를 하기보다는 다양한 사람들의 에너지가 있는 카페나 도서관, 사무실 등에서 더욱 집중이 잘되고 효율적이 됩니다."
            msg3 = "책이나 노트북을 들고 와 카페에 앉아있는 사람들이 왜 그런지 이해가 되시나요? 당신은 외부, 혹은 다른 사람에 대한 관심이 많기 때문에 인간 관계란 무엇인가, 인간 관계는 어떻게 하는 것 인가에 대한 지혜가 있습니다."
            msg4 = "혼자서 작업이나 공부나 일을 하다가 막힘이 있는것처럼 답답함이 있을 때 주변에 사람이 모이거나 혹은 사람들이 있는 장소로 가면 갑자기 집중이 되면서 시간 가는 줄 모르게 집중이 될 수 있습니다. 반드시 동료나 가족이나 가까운 아는 사람들이 아니여도 괜찮습니다. 당신의 두 묶음 에너지 흐름은 타인의 에너지와 함께 연결이 되면 더 자연스럽게 흐르기 때문입니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 46% 분포에 해당됩니다."
            tag = "카페에서도 공부 잘함,사람에 관심이 많아요,사람 많으면 아이디어 UP"
        elif metadata["d"] == 3:
            h_type = "세 묶음 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_3.png"
            msg = "당신은 때론 스스로가 우유부단하다고 느끼거나 혹은 타인으로 부터 그런 말을 듣게 되는 등 당신은 복잡함을 느낄 수 있습니다."
            msg2 = "에너지 흐름이 세 부분으로 나뉘어 흐르고 있기 때문에 무언가를 진행하거나 결정을 내려야 할 때, 그 각각의 다른 묶음들이 각기 다른 주장을 하기 때문입니다. 혼자서 뭔가를 할 때에는 내적 혼란과 갈등을 겪게 됩니다."
            msg3 = "혼자있을 때, 집중하여 일이나 공부가 잘 되지 않는 당신은 자신 이외의 다른 것에 대한 필요를 느끼고 있습니다. 자기만의 공간에서 일이나 공부를 하기보다는 다양한 사람들의 에너지가 있는 카페나 도서관, 사무실 등이 좋습니다. 당신이 가진 나뉘어져 있는 에너지 흐름이 다른 사람들의 연결을 통해 원활하게 흐르게 되기 때문에 더욱 집중이 잘되고 효율적이 됩니다."
            msg4 = "특히 일이나 공부를 하는 중에 갑자기 다시 집중이 되지 않는다고 느낀다면 여러번 자리를 바꾸는 것이 좋을 수 있습니다. 한 곳에서 오래 있는 것은 당신을 답답하게 만들기 때문입니다. 당신은 한 곳에 머무르며, 같은 영향을 주는 사람과 오래 있기가 힘듭니다. 그래서 한 명의 사람을 만나는 것보다는 여러 사람들을 동시에 만나는 것을 선호할 수 있습니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 11% 분포에 해당됩니다."
            tag = "갈대같은 사람,한 곳에서 집중이 힘듦,자리를 바꿔 공부할 것"
        elif metadata["d"] == 4:
            h_type = "네 묶음 흐름"
            img = "https://asset.i-manual.co.kr/static/images/profile/definition/definition_4.png"
            msg = "당신은 우유부단 할 때도 있고 혹은 매우 조급할 때도 있으며 스스로 엄청나게 복잡함을 느낍니다."
            msg2 = "에너지가 네 부분으로 나뉘어 흐르고 있고, 이 각각의 에너지들이 무언가를 하거나 결정을 내려야 할 때, 서로 다른 주장을 하기 때문입니다."
            msg3 = "혼자있을 때, 집중하여 일이나 공부가 잘 되지 않는 당신은 자신 이외의 다른 것에 대한 필요를 느끼고 있습니다. 당신은 자기만의 공간에서 일이나 공부를 하기보다는 다양한 사람들의 에너지가 있는 카페나 도서관, 사무실 등에서 더욱 집중이 잘되고 효율적이 됩니다."
            msg4 = "특히 일이나 공부를 하는 중에 여러번 자리를 바꾸는 것이 좋을 수 있습니다. 한 곳에서 오래 있는 것은 당신을 답답하게 만들기 때문입니다. 당신은 한 곳에 머무르며, 같은 영향을 주는 사람과 오래 있기가 힘듭니다. 그래서 한 명의 사람을 만나는 것보다는 여러 사람들을 동시에 만나는 것을 선호할 수 있습니다."
            msg5 = "이 에너지 흐름을 가진 사람들은 인류의 0.5% 분포에 해당됩니다."
            tag = "우유부단,새로운게 필요해,친구들과 공부할 것"

        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)
        dispatcher.utter_message(msg3)
        #dispatcher.utter_message(msg4)
        #dispatcher.utter_message(msg5)

        #dispatcher.utter_message(json_message = {
        #                         "type": "arrContents", "content": [[msg, msg2], [msg3, msg4], [msg5]], "tags": f'{tag}'})

        #마지막 센터에 밑에 주석 제거

        
        if leading_priority[0]==2:
            return [SlotSet('step', 1), FollowupAction(name='action_question_intro')]
        elif leading_priority[1]==2:
            return [SlotSet('step', 2), FollowupAction(name='action_question_intro')]
        elif leading_priority[2]==2:
            return [SlotSet('step', 3), FollowupAction(name='action_question_intro')]
        elif leading_priority[3]==2:
            return [SlotSet('step', 4), FollowupAction(name='action_question_intro')]

import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, extract_metadata_from_data
from rasa_sdk.events import FollowupAction

logger = logging.getLogger(__name__)

class ActionLastMessage(Action):
    def name(self) -> Text:
        return "action_last_message"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_last_message')

        response = tracker.get_slot('result')
        print(response)
        #metadata = extract_metadata_from_tracker(tracker)
        #select_metadata = tracker.get_slot('select_metadata')
        #metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        # if response == 'yes':
        #     dispatcher.utter_message(
        #         f'다행이예요! 앞으로도 쭉 나답게 잘 살기를 바라요! 잊을만하면 다시 찾아와주세요.')
        # ###아래줄 추가
        # elif response == 'fin_question':
        #     dispatcher.utter_message(
        #         f'궁금증이 해결되셔서 다행이에요! 앞으로도 쭉 나답게 잘 살기를 바라요! 잊을만하면 다시 찾아와주세요.'
        #     )
        # else:
        #     dispatcher.utter_message(
        #         f'불만족스러우셨군요, 좀더 노력해서 좀더 나은 마스터봇이 되어볼게요!')

        dispatcher.utter_message("당신이 타고난 디자인에 대한 마스터봇의 설명이 이해가 잘 되셨나요?")
        dispatcher.utter_message('아이매뉴얼에서 준비한 당신의 설명서를꼼꼼이 읽어보시길 바랍니다.')
        dispatcher.utter_message("그대로 궁금한 점이 있다면 언제든 다시 마스터봇을 호출하여 질문을 해주세요.")
        dispatcher.utter_message("당신이 타고난 디자인대로 행복하게 살 수 있기를 응원합니다. 다시 만나요~")
        #dispatcher.utter_message(
        #    f'제가 다시 필요해진다면, 입력창에 "마스터 봇"을 입력해주세요! 언제든지 기다리고 있을게요 :)')

        return []        

class ActionGoodbye(Action):
    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_goodbye')

        #metadata = extract_metadata_from_tracker(tracker)
        #select_metadata = tracker.get_slot('select_metadata')
        #metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        dispatcher.utter_message(
            f'그럼 {metadata["pn"]}님, 다음에 한번 들러주세요! :) ')

        dispatcher.utter_message(
            f'제가 다시 필요해진다면, 입력창에 "마스터 봇"을 입력해주세요! 언제든지 기다리고 있을게요 :)')

        return []

class ActionMasterbot(Action): #수정필요 entity를 통해 어디부분부터 설명할지
    def name(self) -> Text:
        return "action_masterbot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        
        #metadata = extract_metadata_from_tracker(tracker)
        #select_metadata = tracker.get_slot('select_metadata')
        #metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        leading_priority = tracker.get_slot("leading_priority")
        step = tracker.get_slot("step")
        is_finished = tracker.get_slot("is_finished")
        user_text = tracker.latest_message['text']
        center_step = tracker.get_slot('center_step')
        if(user_text == "마스터 봇" or user_text == "마스터봇"):
            dispatcher.utter_message(
                f'안녕하세요 {metadata["pn"]}님, 저를 부르셨나요~? :) 다시 찾아주셔서 감사해요~')
        #다시 들어왔을 때 판단
        if is_finished==1:
            buttons = []
            buttons.append({"title": "종족", "payload": "/leading_type_intro"})
            buttons.append({"title": "사회적 성향", "payload": "/leading_profile_intro"})
            buttons.append({"title": "에너지 흐름", "payload": "/leading_definition_intro"})
            buttons.append({"title": "센터", "payload": "/leading_centers_intro"})
        
            dispatcher.utter_message("다시 듣고 싶은 항목을 선택해 주세요", buttons=buttons)
        else:
            buttons = []
            buttons.append({"title": "네 이어서 들을래요", "payload": "/leading_masterbot_more"})
            buttons.append({"title": "아뇨! 처음부터 들을래요", "payload": "/initialized"})

            dispatcher.utter_message("지난번에 이어서 들으시겠어요?", buttons=buttons)
        return []
        # dispatcher.utter_message("로케이션 세팅 완료!")


class ActionMasterbotMore(Action):  # 수정필요 entity를 통해 어디부분부터 설명할지
    def name(self) -> Text:
        return "action_masterbot_more"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']

        # metadata = extract_metadata_from_tracker(tracker)
        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)
        metadata = extract_metadata_from_data(tracker)

        leading_priority = tracker.get_slot("leading_priority")
        step = tracker.get_slot("step")
        center_step = tracker.get_slot('center_step')
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

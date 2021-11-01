import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, koelectra_qa_getanswer, extract_metadata_from_data
from actions.sentiment_analysis import sentiment_predict
from rasa_sdk.events import FollowupAction

import pandas as pd

logger = logging.getLogger(__name__)

center_defined_csv = pd.read_csv("./data/center(defined).csv")
center_undefined_csv = pd.read_csv("./data/center(undefined).csv")
definition_csv = pd.read_csv("./data/definition.csv")
profile_csv = pd.read_csv("./data/profile.csv")

type0_csv = pd.read_csv("./data/type(energizer).csv")
type1_csv = pd.read_csv("./data/type(speed energizer).csv")
type2_csv = pd.read_csv("./data/type(revolution).csv")
type3_csv = pd.read_csv("./data/type(guide).csv")
type4_csv = pd.read_csv("./data/type(mirror).csv")

strategy0_csv = pd.read_csv("./data/strategy(energizer).csv")
strategy1_csv = pd.read_csv("./data/strategy(energizer).csv")
strategy2_csv = pd.read_csv("./data/strategy(revolution).csv")
strategy3_csv = pd.read_csv("./data/strategy(guide).csv")
strategy4_csv = pd.read_csv("./data/strategy(mirror).csv")

cd_title = center_defined_csv['title'].values.tolist()
cud_title = center_undefined_csv['title'].values.tolist()
def_title = definition_csv['title'].values.tolist()
prf_title = profile_csv['title'].values.tolist()

cd_paragraph = center_defined_csv['paragraph'].values.tolist()
cud_paragraph = center_undefined_csv['paragraph'].values.tolist()
def_paragraph = definition_csv['paragraph'].values.tolist()
prf_paragraph = profile_csv['paragraph'].values.tolist()

type0_paragraph = type0_csv['paragraph'].values.tolist()
type1_paragraph = type1_csv['paragraph'].values.tolist()
type2_paragraph = type2_csv['paragraph'].values.tolist()
type3_paragraph = type3_csv['paragraph'].values.tolist()
type4_paragraph = type4_csv['paragraph'].values.tolist()

strategy0_paragraph = strategy0_csv['paragraph'].values.tolist()
strategy1_paragraph = strategy1_csv['paragraph'].values.tolist()
strategy2_paragraph = strategy2_csv['paragraph'].values.tolist()
strategy3_paragraph = strategy3_csv['paragraph'].values.tolist()
strategy4_paragraph = strategy4_csv['paragraph'].values.tolist()

center_index = [0, 2, 3, 4, 5, 6]
center_info = ["연료센터", "활력센터", "직관센터", "감정센터", "에고센터", "방향센터", "표현센터", "생각센터", "영감센터"]

def type_retrieve_context(i, context_index):
    type_context = ''
    if i == 0:
        type_context = type0_paragraph[context_index]
    elif i == 1:
        type_context = type1_paragraph[context_index]
    elif i == 2:
        type_context = type2_paragraph[context_index]
    elif i == 3:
        type_context = type3_paragraph[context_index]
    elif i == 4:
        type_context = type4_paragraph[context_index]

    return type_context


def strategy_retrieve_context(i, context_index):
    strategy_context = ''
    if i == 0:
        strategy_context = strategy0_paragraph[context_index]
    elif i == 1:
        strategy_context = strategy1_paragraph[context_index]
    elif i == 2:
        strategy_context = strategy2_paragraph[context_index]
    elif i == 3:
        strategy_context = strategy3_paragraph[context_index]
    elif i == 4:
        strategy_context = strategy4_paragraph[context_index]

    return strategy_context

def retrieve_context(i, ct_index, metadata):
    # 종족은 없음
    # return 할 context
    user_context = ""

    # profile
    if i == 1:

        profile_num = str(metadata["p"])
        profile_str = profile_num[0] + "/" + profile_num[1]
        print(profile_str)

        index = 0
        for t in prf_title:
            if profile_str in t:
                user_context = prf_paragraph[index]
                break
            index += 1

    # definition
    elif i == 2:
        # d는 0: 절전모드, 1: 한묶음, 2: 두묶음, 3: 세묶음, 4: 네묶음
        user_definition = metadata["d"]
        print("user_definition", user_definition)
        user_context = def_paragraph[user_definition]

    # center
    elif i == 3:

        total_center_info = metadata["ct"]
        # 미정의 센터인 경우
        if total_center_info[ct_index] == 0:
            user_context = cud_paragraph[ct_index]
        # 정의 센터인 경우
        else:
            user_context = cd_paragraph[ct_index]
    print(user_context)
    return user_context


class ActionQuestion(Action):
    def name(self) -> Text:
        return "action_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_question')

        #metadata = extract_metadata_from_tracker(tracker)

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)

        leading_priority = tracker.get_slot('leading_priority')
        step = tracker.get_slot('step')
        q_type = leading_priority[step - 1]
        is_question = tracker.get_slot('is_question')
        print("is_question", is_question)
        step = tracker.get_slot("step")
        print(step)
        if is_question==True:
            if q_type == 0:
                return [FollowupAction(name="action_leading_type_question")]
            else:
                dispatcher.utter_message('무엇이 궁금하신가요?')
        else:
            return [SlotSet("is_question", False), FollowupAction(name="action_default_fallback")]
        h_type = ''

        return [SlotSet("step", step), SlotSet("is_question", True)]


class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('action_default_fallback')

        #metadata = extract_metadata_from_tracker(tracker)

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)

        user_reponse_type = 0
        # 질문인지 아닌지(0이면 질문아님, 1이면 질문)
        is_question = tracker.get_slot("is_question")
        print("is_question", is_question)
        # 감정분석인지 아닌지(0이면 아님, 1이면 감정분석)
        is_sentiment = tracker.get_slot("is_sentiment")
        print("is_sentiment", is_sentiment)

        center_question = tracker.get_slot("center_question")
        user_text = tracker.latest_message['text']
        question = tracker.get_slot("bot_question")
        ct_index = tracker.get_slot("center_type")
        center_step = tracker.get_slot("center_step")
        # tracker 에서 필요한 변수 load
        leading_priority = tracker.get_slot('leading_priority')

        step = tracker.get_slot("step")
        print("step", step)
        answer = ""
        # 설명 완료한 개수-> step
        # 방금 설명한 파트는 step - 1의 인덱스를 가짐
        if is_question==True:
            q_type = leading_priority[step - 1]

            answer = ""
            # 내담자의 정보에 해당하는 context를 가져옴
            context = retrieve_context(q_type, ct_index=ct_index, metadata=metadata)
            # QA 모듈
            answer = koelectra_qa_getanswer(context, user_text)
            print(answer)

        else:
            if is_sentiment:
                user_reponse_type = sentiment_predict(question, user_text)
                if user_reponse_type == 0:
                    print("중립")
                    answer = "비자아 코멘트(중립)"
                elif user_reponse_type == 1:
                    print("긍정")
                    answer = "축하합니다. 당신의 센터는 건강합니다."
                elif user_reponse_type == 2:
                    print("부정")
                    answer = "비자아 코멘트"

        # 올바른 질문이 아닌경우
        if is_question==True and answer == "":
            # 다시 action_default_fallback으로 넘어오는 분기 필요!!
            answer = "질문을 잘 못 알아들었어요"

            dispatcher.utter_message(answer)
            buttons = []
            buttons.append({"title": f'질문', "payload": "/question{\"is_question\":\"True\"}"})
            buttons.append({"title": f'괜찮아요', "payload": "/leading_more"})
            dispatcher.utter_message("다시 질문하고 싶으시면 질문 버튼을 클릭해주세요!", buttons=buttons)
            return [SlotSet("step", step)]

        # QA이면
        if is_question==True:
            print("center_question : ", center_question)
            qa_buttons = []
            # 센터 질문이면
            if center_question==True:
                qa_buttons.append({"title": f'확인', "payload": "/center_unego_question"})
                qa_buttons.append({"title": f'아뇨! 더 질문할래요', "payload": "/question{\"is_question\":\"True\", \"center_question\":\"True\"}"})
            # 센터 질문이 아니면
            else:
                qa_buttons.append({"title": f'확인', "payload": "/leading_more"})
                qa_buttons.append({"title": f'아뇨! 더 질문할래요', "payload": "/question{\"is_question\":\"True\"}"})

            dispatcher.utter_message(f'{answer}')
            dispatcher.utter_message(f'궁금증이 풀리셨나요?', buttons=qa_buttons)

        # 감정분석이면
        else:
            print("center step", center_step)
            if is_sentiment==True:
                dispatcher.utter_message(answer)
                if center_step < 8:
                    center_step += 1
                    return [SlotSet("step", step), SlotSet("is_question", False), SlotSet("is_sentiment", False), SlotSet("center_step", center_step), FollowupAction(name='action_leading_centers_intro')]
                else:
                    return [SlotSet("step", step), SlotSet("is_question", False), SlotSet("is_sentiment", False), SlotSet("center_step", center_step), FollowupAction(name='action_more')]
            else:
                notice_buttons = []
                notice_buttons.append({"title": f'질문', "payload": "/question{\"is_question\":\"True\"}"})
                notice_buttons.append({"title": f'괜찮아요', "payload": "/leading_more"})

                notice = '''지금은 채팅하실 수 없습니다. 혹시 질문 있으신가요?'''
                dispatcher.utter_message(f'{notice}', buttons=notice_buttons)



        return [SlotSet("step", step), SlotSet("is_question", False), SlotSet("is_sentiment", False)]

class ActionQuestionIntro(Action):
    def name(self):
        return "action_question_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_question_intro')
        #metadata = extract_metadata_from_tracker(tracker)

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)

        human_types = ["에너자이저 종족", "스피드 에너자이저 종족", "혁신주도가 종족", "가이드 종족", "거울 종족"]
        human_definition = ["절전모드", "한 묶음 흐름", "두 묶음 흐름", "세 묶음 흐름", "네 묶음 흐름"]
        human_center = ["연료센터", "활력센터", "직관센터", "감정센터", "에고센터", "방향센터", "표현센터", "생각센터", "영감센터"]
        human_profile = {13: "1/3", 14: "1/4", 24: "2/4",
                         25:"2/5", 35:"3/5", 36:"3/6",
                         41:"4/1", 46:"4/6", 51:"5/1",
                         52:"5/2", 62:"6/2", 63:"6/3"}
        step = tracker.get_slot("step")
        is_question = tracker.get_slot("is_question")
        center_question = tracker.get_slot("center_question")
        center_priority = tracker.get_slot("center_priority")
        ct_index = tracker.get_slot("center_type")
        center_step = tracker.get_slot("center_step")
        # tracker 에서 필요한 변수 load
        leading_priority = tracker.get_slot('leading_priority')
        q_type = leading_priority[step - 1]

        is_center = False
        is_type = False

        bot_text = ''
        # 종족
        if q_type == 0:
            is_type = True
            bot_text = f"자, {human_types[metadata['t']]}에 대해 질문있으신가요?"
        # 프로파일
        elif q_type == 1:
            bot_text = f"자, {human_profile[metadata['p']]} 성향에 대해 질문있으신가요?"
        # 에너지흐름
        elif q_type == 2:
            bot_text = f"{human_definition[metadata['d']]}에 대해 질문있으신가요?"
        # 센터
        elif q_type == 3:
            is_center = True
            tmp_index = center_priority[center_step]
            if metadata['ct'][tmp_index] == 0:
                bot_text = f"{human_center[tmp_index]} (미정의)에 대해 질문있으신가요?"
            else:
                bot_text = f"{human_center[tmp_index]} (정의)에 대해 질문있으신가요?"

        buttons = []
        if is_type:
            buttons.append({"title": f'네. 질문 있어요', "payload": "/leading_type_question"})
        else:
            buttons.append({"title": f'네. 질문 있어요', "payload": "/question{\"is_question\":\"True\"}"})

        if is_center:
            if center_step == 9:
                buttons.append({"title": f'아뇨 질문 없어요', "payload": "/leading_centers_question"})
            else:
                buttons.append({"title": f'아뇨 질문 없어요', "payload": "/center_unego_question"})
        else:
            buttons.append({"title": f'아뇨 질문 없어요', "payload": "/leading_more"})

        dispatcher.utter_message(bot_text, buttons=buttons)

        if is_center:
            return [SlotSet("center_question", True)]
        else:
            return [SlotSet("center_question", False)]

class ActionTypeQuestion(Action):
    def name(self):
        return "action_type_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_type_question')
        #metadata = extract_metadata_from_tracker(tracker)

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)

        type_index = metadata["t"]
        question = tracker.get_slot("bot_question")
        context_index = tracker.get_slot("context_index")
        step = tracker.get_slot("step")
        print(step)

        context = type_retrieve_context(type_index, context_index=context_index)
        answer = koelectra_qa_getanswer(context, question)
        dispatcher.utter_message(answer)

        buttons = []
        buttons.append({"title": f'궁금증이 풀렸어요!', "payload": "/leading_more"})
        buttons.append({"title": f'아뇨! 다른 질문도 할래요', "payload": "/leading_type_question"})
        dispatcher.utter_message(f'궁금증이 풀리셨나요?', buttons=buttons)

class ActionStrategyQuestion(Action):
    def name(self):
        return "action_strategy_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_strategy_question')
        #metadata = extract_metadata_from_tracker(tracker)

        select_metadata = tracker.get_slot('select_metadata')
        metadata = extract_metadata_from_data(select_metadata)

        type_index = metadata["t"]
        question = tracker.get_slot("bot_question")
        context_index = tracker.get_slot("context_index")
        step = tracker.get_slot("step")
        print(step)

        context = strategy_retrieve_context(type_index, context_index=context_index)
        print(context)
        answer = koelectra_qa_getanswer(context, question)
        print(answer)
        dispatcher.utter_message(answer)

        buttons = []
        buttons.append({"title": f'궁금증이 풀렸어요!', "payload": "/leading_more"})
        buttons.append({"title": f'아뇨! 다른 질문도 할래요', "payload": "/leading_type_question"})
        dispatcher.utter_message(f'궁금증이 풀리셨나요?', buttons=buttons)

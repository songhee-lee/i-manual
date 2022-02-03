import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker, koelectra_qa_getanswer, unego_get_question, \
    sentiment_get_ego_or_unego, unego_answer
from actions.sentiment_analysis import sentiment_predict
from rasa_sdk.events import FollowupAction

import pandas as pd

unego_description_csv = pd.read_csv("./data/자아_비자아 question.csv")
unego_description = unego_description_csv['paragraph'].values.tolist()

etc_description_csv = pd.read_csv("./data/기타.csv")
etc_description = etc_description_csv['paragraph'].values.tolist()
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
center_info = ["연료 센터", "활력 센터", "직관 센터", "감정 센터", "에고 센터", "방향 센터", "표현 센터", "생각 센터", "영감 센터"]


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

        metadata = extract_metadata_from_tracker(tracker)

        leading_priority = tracker.get_slot('leading_priority')
        is_question = tracker.get_slot('is_question')
        print("is_question", is_question)
        step = tracker.get_slot("step")
        print(step)
        center_question = tracker.get_slot("center_question")

        if leading_priority is None or step is None or is_question is None or center_question is None:
            return [FollowupAction(name='action_set_priority_again')]

        q_type = leading_priority[step - 1]
        if is_question:
            if q_type == 0:
                return [FollowupAction(name="action_leading_type_question")]
            else:
                dispatcher.utter_message(etc_description[5])
        else:
            return [SlotSet("is_question", 0), FollowupAction(name="action_default_fallback")]

        return [SlotSet("step", step), SlotSet("is_question", 1)]


class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('action_default_fallback')

        metadata = extract_metadata_from_tracker(tracker)

        user_reponse_type = 0
        # 질문인지 아닌지(0이면 질문아님, 1이면 질문)
        is_question = tracker.get_slot("is_question")
        print("is_question", is_question)
        # 감정분석인지 아닌지(0이면 아님, 1이면 감정분석)
        is_sentiment = tracker.get_slot("is_sentiment")
        print("is_sentiment", is_sentiment)

        center_question = tracker.get_slot("center_question")
        print("before QA center question", center_question)
        user_text = tracker.latest_message['text']
        question = tracker.get_slot("bot_question")
        ct_index = tracker.get_slot("center_type")
        center_step = tracker.get_slot("center_step")
        # tracker 에서 필요한 변수 load
        leading_priority = tracker.get_slot('leading_priority')
        center_priority = tracker.get_slot("center_priority")
        center_type = tracker.get_slot('center_type')
        step = tracker.get_slot("step")
        unego_count = tracker.get_slot("unego_count")
        sentiment_result = tracker.get_slot("sentiment_result")
        ego_or_unego = tracker.get_slot("ego_or_unego")
        if is_question is None or is_sentiment is None or center_question is None or leading_priority is None or center_priority is None or step is None or ego_or_unego is None:
            return [FollowupAction(name='action_set_priority_again')]
        print("step", step)
        answer = ""
        opposite_question = ["다른 사람의 감정 변화를 잘 캐치하고 눈치껏 침묵하며 기다려주는 편인가요?",
                             "기분에 따라 충동적으로 의사결정을 하기보다 충분한 시간을 갖고 생각하는 편인가요?",
                             "결과를 깊게 생각하기 보다 즉각적인 '촉'을 따르는 경우가 많나요?", "나에게 좋지 못한 관계나 일에 엮이면 단호하게 끊어내는 편인가요?",
                             "아무리 바빠도 내가 사랑하는 일이라면 즐겁고 행복한가요?", "지키지 못할 약속은 하지 않는 편인가요?",
                             "운명의 짝이라면 엄청난 노력을 쏟아붓지 않아도 나타날 것이라 생각하는 편인가요?", "내가 하고 싶은 것, 원하는 것이 뚜렷한 편인가요?",
                             "나는 취향이 확고한 편인가요?", "흥미로운 정보를 발견하면 시간 가는 줄 모르고 빠져드는 편인가요?"]
        yes_list = ["네", "네 맞아요", "네맞아요", "맞아요", "당연하죠", "당연하지", "그런 것 같아요", "그런것같아요", "그런것 같아요", "그런거같아요", "그런거 같아요",
                    "그런거같아", "그런 거 같아", "맞아", "응", "응맞아", "응 맞아", "그치", "그래요", "그래", "네 그런편이에요", "그런편이에요", "예", "네네",
                    "웅", "응응", "그렇죠", "맞는거같아요", "그런듯", "완전 맞아요", "넹", "완전 그래요", "ㅇㅇ", "ㅇ", "yes", "yeah", "y"]
        no_list = ["아니요", "아뇨", "아니에요", "아녜요", "아닙니다", "아니", "안그래", "전혀 아니야", "전혀아님", "아님", "아니 그렇진 않아", "아닌 것 같아",
                   "아닌것 같아", "아닌것같아", "아닌거같아", "아닌거 같아", "아닌 거 같아", "아닌 것 같아요", "아닌것 같아요", "아닌것같아요", "아닌거같아요",
                   "아닌 거 같아요", "아닌거 같아요", "전혀", "아니!", "아니요.", "아니.", "ㄴㄴ", "ㄴ", "no", "nono", "n", "절대 아니야", "아니 전혀",
                   "놉", "노", "노노", "안그래", "안히", "안니", "않니", "그럴리가", "그럴리가요"]
        neutral_list = ["모르겠어요", "몰라요", "몰라", "모르겠어", "잘 몰라", "잘몰라", "잘 모르겠어", "잘모르겠어", "잘몰라요", "잘 몰라요", "잘 모르겠어요",
                        "잘모르겠어요", "글쎄", "글쎄요"]
        # 설명 완료한 개수-> step
        # 방금 설명한 파트는 step - 1의 인덱스를 가짐
        if is_question:
            q_type = leading_priority[step - 1]

            qa_step = ""
            if q_type == 1:
                qa_step = "프로파일"
            elif q_type == 2:
                qa_step = "에너지 흐름"

            elif q_type == 3:
                if center_priority[center_step] == 0 and metadata["ct"][0] == 0:
                    qa_step = "연료센터(미정의)"
                elif center_priority[center_step] == 0 and metadata["ct"][0] == 1:
                    qa_step = "연료센터(정의)"

                elif center_priority[center_step] == 1 and metadata["ct"][1] == 0:
                    qa_step = "활력센터(미정의)"
                elif center_priority[center_step] == 1 and metadata["ct"][1] == 1:
                    qa_step = "활력센터(정의)"

                elif center_priority[center_step] == 2 and metadata["ct"][2] == 0:
                    qa_step = "직관센터(미정의)"
                elif center_priority[center_step] == 2 and metadata["ct"][2] == 1:
                    qa_step = "직관센터(정의)"

                elif center_priority[center_step] == 3 and metadata["ct"][3] == 0:
                    qa_step = "감정센터(미정의)"
                elif center_priority[center_step] == 3 and metadata["ct"][3] == 1:
                    qa_step = "감정센터(정의)"

                elif center_priority[center_step] == 4 and metadata["ct"][4] == 0:
                    qa_step = "에고센터(미정의)"
                elif center_priority[center_step] == 4 and metadata["ct"][4] == 1:
                    qa_step = "에고센터(정의)"

                elif center_priority[center_step] == 5 and metadata["ct"][5] == 0:
                    qa_step = "방향센터(미정의)"
                elif center_priority[center_step] == 5 and metadata["ct"][5] == 1:
                    qa_step = "방향센터(정의)"

                elif center_priority[center_step] == 6 and metadata["ct"][6] == 0:
                    qa_step = "표현센터(미정의)"
                elif center_priority[center_step] == 6 and metadata["ct"][6] == 1:
                    qa_step = "표현센터(정의)"

                elif center_priority[center_step] == 7 and metadata["ct"][7] == 0:
                    qa_step = "생각센터(미정의)"
                elif center_priority[center_step] == 7 and metadata["ct"][7] == 1:
                    qa_step = "생각센터(정의)"

                elif center_priority[center_step] == 8 and metadata["ct"][8] == 0:
                    qa_step = "영감센터(미정의)"
                elif center_priority[center_step] == 8 and metadata["ct"][8] == 1:
                    qa_step = "영감센터(정의)"

            print("qa_step = ", qa_step)

            answer = ""
            # 내담자의 정보에 해당하는 context를 가져옴
            context = retrieve_context(q_type, ct_index=ct_index, metadata=metadata)
            # QA 모듈

            answer = koelectra_qa_getanswer(context, user_text, metadata=metadata, qa_step=qa_step)

            print(answer)
            qa_step = ""

        else:
            if is_sentiment:
                # 0:중립, 1:비자아, 2:자아
                if user_text in yes_list:
                    user_reponse_type = 1
                elif user_text in no_list:
                    user_reponse_type = 2
                elif user_text in neutral_list:
                    user_response_type = 0
                else:
                    user_reponse_type = sentiment_predict(question, user_text)

                if user_reponse_type == 0:
                    print("중립")
                elif user_reponse_type == 1:  # 긍정
                    if question not in opposite_question:
                        print("비자아")
                        sentiment_result -= 1
                    else:
                        print("자아")
                        sentiment_result += 1
                elif user_reponse_type == 2:  # 부정
                    if question not in opposite_question:
                        print("자아")
                        sentiment_result += 1
                    else:
                        print("비자아")
                        sentiment_result -= 1

        # 올바른 질문이 아닌경우
        if is_question and answer == "":
            # 다시 action_default_fallback으로 넘어오는 분기 필요!!
            answer = etc_description[7]

            dispatcher.utter_message(answer)
            buttons = []
            if center_question == 1:
                buttons.append(
                    {"title": f'질문 있어요', "payload": "/question{\"is_question\":1, \"center_question\":1}"})
                buttons.append({"title": f'질문 없어요', "payload": "/center_unego_question"})
            else:
                buttons.append(
                    {"title": f'질문 있어요', "payload": "/question{\"is_question\":1, \"center_question\":0}"})
                buttons.append({"title": f'질문 없어요', "payload": "/leading_more"})
            dispatcher.utter_message(etc_description[4], buttons=buttons)
            return [SlotSet("step", step)]

        # QA이면
        if is_question == 1:
            qa_buttons = []
            # 센터 질문이면
            print("after QA center question", center_question)
            if center_question == 1:
                qa_buttons.append(
                    {"title": f'질문 있어요', "payload": "/question{\"is_question\":1, \"center_question\":1}"})
                qa_buttons.append(
                    {"title": f'질문 없어요', "payload": "/center_unego_question{\"is_question\":0, \"center_question\":0}"})
            # 센터 질문이 아니면
            else:
                qa_buttons.append(
                    {"title": f'질문 있어요', "payload": "/question{\"is_question\":1, \"center_question\":0}"})
                qa_buttons.append(
                    {"title": f'질문 없어요', "payload": "/leading_more{\"is_question\":0, \"center_question\":0}"})

            dispatcher.utter_message(f'{answer}')
            dispatcher.utter_message(etc_description[6], buttons=qa_buttons)

        # 감정분석이면
        else:
            print("center step", center_step)
            if is_sentiment:
                dispatcher.utter_message(answer)
                # 비자아 질문 3개 다한 경우
                if unego_count == 3:
                    if metadata['ct'][center_type] == 0:
                        unego_question = unego_get_question(center_type, unego_count - 1, defined=False)
                    else:
                        unego_question = unego_get_question(center_type, unego_count - 1, defined=True)

                    # 자아인 경우
                    if sentiment_result > 0:
                        dispatcher.utter_message(unego_description[91])
                        answer = unego_question[1]
                        ego_or_unego[center_priority[center_step]] = 1
                        print("ego_or_unego : ", ego_or_unego)
                        sentiment_get_ego_or_unego(ego_or_unego, metadata)
                        unego_answer(question, user_text, metadata)
                    # 비자아 혹은 중립인 경우
                    else:
                        message = unego_description[92].format(center_info[center_type])
                        dispatcher.utter_message(message)
                        answer = unego_question[2]
                        ego_or_unego[center_priority[center_step]] = -1
                        sentiment_get_ego_or_unego(ego_or_unego, metadata)
                        unego_answer(question, user_text, metadata)

                    dispatcher.utter_message(answer)
                    return [SlotSet("sentiment_result", 0), SlotSet("ego_or_unego", ego_or_unego),
                            FollowupAction(name='action_center_unego_question')]
                else:
                    return [SlotSet("sentiment_result", sentiment_result),
                            FollowupAction(name='action_center_unego_question')]
            else:
                notice_buttons = []
                if center_question == 1:
                    notice_buttons.append(
                        {"title": f'질문 있어요', "payload": "/question{\"is_question\":1, \"center_question\":1}"})
                else:
                    notice_buttons.append(
                        {"title": f'질문 있어요', "payload": "/question{\"is_question\":1, \"center_question\":0}"})

                notice_buttons.append(
                    {"title": f'질문 없어요', "payload": "/leading_more{\"is_question\":0, \"center_question\":0}"})

                notice = etc_description[8]
                notice2 = etc_description[9]
                dispatcher.utter_message(f'{notice}')
                dispatcher.utter_message(f'{notice2}', buttons=notice_buttons)

        return [SlotSet("step", step), SlotSet("is_sentiment", 0), SlotSet("ego_or_unego", ego_or_unego)]


class ActionQuestionIntro(Action):
    def name(self):
        return "action_question_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_question_intro')
        metadata = extract_metadata_from_tracker(tracker)

        human_types = ["에너자이저 종족", "스피드 에너자이저 종족", "혁신주도가 종족", "가이드 종족", "거울 종족"]
        human_definition = ["절전모드", "한 묶음 흐름", "두 묶음 흐름", "세 묶음 흐름", "네 묶음 흐름"]
        human_center = ["연료센터", "활력센터", "직관센터", "감정센터", "에고센터", "방향센터", "표현센터", "생각센터", "영감센터"]
        human_profile = {13: "1/3", 14: "1/4", 24: "2/4",
                         25: "2/5", 35: "3/5", 36: "3/6",
                         41: "4/1", 46: "4/6", 51: "5/1",
                         52: "5/2", 62: "6/2", 63: "6/3"}
        step = tracker.get_slot("step")
        is_question = tracker.get_slot("is_question")
        center_question = tracker.get_slot("center_question")
        center_priority = tracker.get_slot("center_priority")
        ct_index = tracker.get_slot("center_type")
        center_step = tracker.get_slot("center_step")
        # tracker 에서 필요한 변수 load
        leading_priority = tracker.get_slot('leading_priority')
        if step is None or center_step is None or leading_priority is None:
            return [FollowupAction(name='action_set_priority_again')]
        q_type = leading_priority[step - 1]

        is_center = 0
        is_type = 0

        bot_text = ''
        # 종족
        if q_type == 0:
            is_type = 1

        elif q_type == 3:
            is_center = 1

        buttons = []
        if is_type:
            buttons.append({"title": f'질문 있어요', "payload": "/leading_type_question"})
        else:
            buttons.append({"title": f'질문 있어요', "payload": "/question{\"is_question\":\"1\"}"})

        if is_center:
            if center_step == 9:
                buttons.append({"title": f'질문 없어요', "payload": "/leading_centers_question"})
            else:
                buttons.append({"title": f'질문 없어요', "payload": "/center_unego_question"})
        else:
            buttons.append({"title": f'질문 없어요', "payload": "/leading_more"})

        dispatcher.utter_message(etc_description[4], buttons=buttons)

        if is_center:
            return [SlotSet("center_question", 1)]
        else:
            return [SlotSet("center_question", 0)]


class ActionCenterUnegoQuestion(Action):
    def name(self) -> Text:
        return "action_center_unego_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_center_unego_question')
        human_center = ["연료센터", "활력센터", "직관센터", "감정센터", "에고센터", "방향센터", "표현센터", "생각센터", "영감센터"]
        metadata = extract_metadata_from_tracker(tracker)

        user_text = tracker.latest_message['text']
        question = tracker.get_slot("bot_question")

        center_type = tracker.get_slot("center_type")
        center_step = tracker.get_slot("center_step")
        # 비자아 질문 개수 확인
        unego_count = tracker.get_slot("unego_count")
        # default 값이 0이므로 시작 count 를 1로 설정.
        unego_count += 1
        step = tracker.get_slot("step")
        print(step)
        if center_type is None or center_step is None or unego_count is None or step is None:
            return [FollowupAction(name='action_set_priority_again')]
        unego_question = ''
        print("unego_count : ", unego_count)
        if unego_count < 4:
            if metadata['ct'][center_type] == 0:
                unego_question = unego_get_question(center_type, unego_count - 1, defined=False)
            else:
                unego_question = unego_get_question(center_type, unego_count - 1, defined=True)

            # 조건화 질문 시작시 멘트
            if unego_count == 1:
                message = unego_description[90].format(human_center[center_type])
                dispatcher.utter_message(message)
                
            # 0번째가 질문, 1번째가 자아 멘트, 2번째가 비자아
            dispatcher.utter_message(unego_question[0])

            if unego_count>1:

                unego_answer(question, user_text, metadata)


            return [SlotSet('bot_question', unego_question[0]), SlotSet("is_question", 0),
                    SlotSet("center_question", 1), SlotSet("is_sentiment", 1), SlotSet("unego_count", unego_count)]

        return [SlotSet("is_question", 0), SlotSet("center_type", center_type), SlotSet("center_step", center_step + 1),
                SlotSet("center_question", 1), SlotSet("step", step), SlotSet("is_sentiment", 1),
                SlotSet("unego_count", 0), FollowupAction(name="action_more")]


class ActionTypeQuestion(Action):
    def name(self):
        return "action_type_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_type_question')
        metadata = extract_metadata_from_tracker(tracker)

        type_index = metadata["t"]
        question = tracker.get_slot("bot_question")
        context_index = tracker.get_slot("context_index")
        step = tracker.get_slot("step")
        if step is None or question is None or context_index is None:
            return [FollowupAction(name='action_set_priority_again')]
        print(step)

        context = type_retrieve_context(type_index, context_index=context_index)
        answer = koelectra_qa_getanswer(context, question, metadata=metadata)
        dispatcher.utter_message(answer)

        buttons = []
        buttons.append({"title": f'질문 있어요', "payload": "/leading_type_question"})
        buttons.append({"title": f'질문 없어요', "payload": "/leading_more"})
        dispatcher.utter_message(etc_description[6], buttons=buttons)


class ActionStrategyQuestion(Action):
    def name(self):
        return "action_strategy_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_strategy_question')
        metadata = extract_metadata_from_tracker(tracker)

        type_index = metadata["t"]
        question = tracker.get_slot("bot_question")
        context_index = tracker.get_slot("context_index")
        step = tracker.get_slot("step")
        if question is None or context_index is None or step is None:
            return [FollowupAction(name='action_set_priority_again')]
        print(step)

        context = strategy_retrieve_context(type_index, context_index=context_index)
        print(context)
        answer = koelectra_qa_getanswer(context, question)
        print(answer)
        dispatcher.utter_message(answer)

        buttons = []
        buttons.append({"title": f'질문 있어요', "payload": "/leading_type_question"})
        buttons.append({"title": f'질문 없어요', "payload": "/leading_more"})
        dispatcher.utter_message(etc_description[6], buttons=buttons)

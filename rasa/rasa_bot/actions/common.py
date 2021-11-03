from transformers import BertTokenizer, BertForQuestionAnswering, AutoConfig
import torch
import pandas as pd
import random

model_path = "songhee/i-manual-mbert"
config = AutoConfig.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForQuestionAnswering.from_pretrained(model_path, config=config)
def extract_metadata_from_data(num):
    metadata = {}
    if num==1:
        metadata = {"pn": "001", "ct": [1, 0, 1, 0, 0, 1, 1, 0, 0], "se": [1, 2, 0, 6], "t": 3, "p": 14, "d": 2}
    elif num==2:
        metadata = {"pn": "002", "ct": [0, 0, 1, 0, 0, 1, 1, 1, 1], "se": [0, 6, 2, 1], "t": 3, "p": 13, "d": 2}
    elif num==3:
        metadata = {"pn": "003", "ct": [1, 0, 1, 1, 1, 0, 1, 0, 0], "se": [6, 1, 3, 7], "t": 2, "p": 41, "d": 1}
    elif num==4:
        metadata = {"pn": "004", "ct": [0, 0, 0, 1, 0, 0, 1, 0, 0], "se": [3, 3, 7, 6], "t": 2, "p": 24, "d": 1}
    elif num==5:
        metadata = {"pn": "005", "ct": [0, 0, 0, 0, 0, 0, 0, 0, 0], "se": [1, 3, 6, 1], "t": 4, "p": 51, "d": 0}
    elif num==6:
        metadata = {"pn": "006", "ct": [0, 0, 0, 0, 0, 0, 0, 0, 0], "se": [5, 5, 5, 5], "t": 4, "p": 24, "d": 0}
    elif num==7:
        metadata = {"pn": "007", "ct": [0, 1, 1, 1, 0, 1, 1, 0, 0], "se": [1, 6, 1, 3], "t": 0, "p": 52, "d": 2}
    elif num==8:
        metadata = {"pn": "008", "ct": [1, 1, 0, 1, 1, 0, 0, 0, 0], "se": [4, 3, 6, 1], "t": 0, "p": 62, "d": 2}
    elif num==9:
        metadata = {"pn": "009", "ct": [1, 1, 1, 1, 1, 1, 1, 1, 1], "se": [3, 1, 1, 6], "t": 1, "p": 36, "d": 3}
    elif num==10:
        metadata = {"pn": "001", "ct": [1, 1, 1, 0, 0, 1, 1, 1, 0], "se": [2, 1, 6, 0], "t": 1, "p": 35, "d": 1}
    else:
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "se": [2, 0, 6], "t": 3, "p": 52, "d": 3}
    return metadata
def extract_metadata_from_tracker(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']

def koelectra_qa_getanswer(context, question):

    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    answer_start_scores, answer_end_scores = model(**inputs)
    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(
        answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer

def unego_get_question(ct, unego_count, defined=False):
    question = ""
    # 0: 연료, 1: 활력, 2: 직관, 3: 감정, 4: 에고, 5: 방향, 6: 표현, 7: 생각, 8: 영감
    # 연료센터
    if ct == 0 and not defined:
        qlist_0 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_0[unego_count]
        ego_comment = "연료센터(미정) 자아 코멘트"
        unego_comment = "연료센터(미정) 비자아 코멘트"

    elif ct == 0 and defined:
        qlist_0 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_0[unego_count]
        ego_comment = "연료센터(정의) 자아 코멘트"
        unego_comment = "연료센터(정의) 비자아 코멘트"
    # 활력센터
    elif ct == 1 and not defined:
        qlist_1 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_1[unego_count]
        ego_comment = "활력센터(미정) 자아 코멘트"
        unego_comment = "활력센터(미정) 비자아 코멘트"
    elif ct == 1 and defined:
        qlist_1 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_1[unego_count]
        ego_comment = "활력센터(정의) 자아 코멘트"
        unego_comment = "활력센터(정의) 비자아 코멘트"
    # 직관센터
    elif ct == 2 and not defined:
        qlist_2 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_2[unego_count]
        ego_comment = "직관센터(미정) 자아 코멘트"
        unego_comment = "직관센터(미정) 비자아 코멘트"

    elif ct == 2 and defined:
        qlist_2 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_2[unego_count]
        ego_comment = "직관센터(정의) 자아 코멘트"
        unego_comment = "직관센터(정의) 비자아 코멘트"

    # 감정센터
    elif ct == 3 and not defined:
        qlist_3 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_3[unego_count]
        ego_comment = "감정센터(미정) 자아 코멘트"
        unego_comment = "감정센터(미정) 비자아 코멘트"

    elif ct == 3 and defined:
        qlist_3 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_3[unego_count]
        ego_comment = "감정센터(정의) 자아 코멘트"
        unego_comment = "감정센터(정의) 비자아 코멘트"
    # 에고센터
    elif ct == 4 and not defined:
        qlist_4 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_4[unego_count]
        ego_comment = "에고센터(미정) 자아 코멘트"
        unego_comment = "에고센터(미정) 비자아 코멘트"

    elif ct == 4 and defined:
        qlist_4 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_4[unego_count]
        ego_comment = "에고센터(정의) 자아 코멘트"
        unego_comment = "에고센터(정의) 비자아 코멘트"

    # 방향센터
    elif ct == 5 and not defined:
        qlist_5 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_5[unego_count]
        ego_comment = "방향센터(미정) 자아 코멘트"
        unego_comment = "방향센터(미정) 비자아 코멘트"

    elif ct == 5 and defined:
        qlist_5 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_5[unego_count]
        ego_comment = "방향센터(정의) 자아 코멘트"
        unego_comment = "방향센터(정의) 비자아 코멘트"

    # 표현센터
    elif ct == 6 and not defined:
        qlist_6 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_6[unego_count]
        ego_comment = "표현센터(미정) 자아 코멘트"
        unego_comment = "표현센터(미정) 비자아 코멘트"

    elif ct == 6 and defined:
        qlist_6 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_6[unego_count]
        ego_comment = "표현센터(정의) 자아 코멘트"
        unego_comment = "표현센터(정의) 비자아 코멘트"

    # 생각센터
    elif ct == 7 and not defined:
        qlist_7 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_7[unego_count]
        ego_comment = "생각센터(미정) 자아 코멘트"
        unego_comment = "생각센터(미정) 비자아 코멘트"

    elif ct == 7 and defined:
        qlist_7 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_7[unego_count]
        ego_comment = "생각센터(정의) 자아 코멘트"
        unego_comment = "생각센터(정의) 비자아 코멘트"

    # 영감센터
    elif ct == 8 and not defined:
        qlist_8 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_8[unego_count]
        ego_comment = "영감센터(미정) 자아 코멘트"
        unego_comment = "영감센터(미정) 비자아 코멘트"

    elif ct == 8 and defined:
        qlist_8 = [
            "비자아 질문 1",
            "비자아 질문 2",
            "비자아 질문 3"
        ]
        question = qlist_8[unego_count]
        ego_comment = "영감센터(정의) 자아 코멘트"
        unego_comment = "영감센터(정의) 비자아 코멘트"

    question_intro = [
        "제가 질문 한가지 할게요! 질문을 보시고 솔직하게 답변해주시면 됩니다 :)",
        "지금까지 설명을 토대로 내담자님의 성향에 대해서 한가지 질문할게요!!",
        "잘 따라오고 계신가요? 내담자님의 성향을 파악하기 위해서 질문 하나 드릴게요 :)"
    ]
    q_intro = random.choice(question_intro)
    return [q_intro, question, ego_comment, unego_comment]

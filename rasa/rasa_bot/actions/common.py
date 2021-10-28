from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import pandas as pd
import random

model_path = "songhee/i-manual-mbert"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForQuestionAnswering.from_pretrained(model_path, return_dict=False)

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

def unego_get_question(ct, defined=False):
    question = ""
    # 0: 연료, 1: 직관, 2: 감정, 3: 에고, 4: 방향, 5: 표현
    # 연료센터
    if ct == 0 and not defined:
        qlist_0 = [
            "본인은 사람들에게 주목받으려고 애쓰는 편인가요?",
            "본인은 말을 하지 하지 않아도 될 상황에서 대화를 트려고 애쓰는 편인가요?",
            "본인은 늘 먼저 나서서 말을 하려고 하며 의사결정을 내려야 한다고 생각하시나요?"
        ]
        question = random.choice(qlist_0)
    elif ct == 0 and defined:
        qlist_0 = [
            "연료 센터 (정의) 비자아 질문"
        ]
        question = random.choice(qlist_0)
    # 직관센터
    elif ct == 2 and not defined:
        qlist_1 = [
            "나에게 좋지 않은 관계나 일이나 장소등에 집착하고 의지하고 있지는 않은가요?",
        ]
        question = random.choice(qlist_1)
    elif ct == 2 and defined:
        qlist_1 = [
            "직관 센터 (정의) 비자아 질문"
        ]
        question = random.choice(qlist_1)
    # 감정센터
    elif ct == 3 and not defined:
        qlist_2 = [
            "본인은 두려워서 차라리 말을 안하고 있나요?",
            "본인은 말을 해서 화가 나게 될 것 같으면 차라리 말을 말자라며 혼자 끙끙하나요?"
        ]
        question = random.choice(qlist_2)
    elif ct == 3 and defined:
        qlist_2 = [
            "감정 센터 (정의) 비자아 질문"
        ]
        question = random.choice(qlist_2)

    # 에고센터
    elif ct == 4 and not defined:
        qlist_3 = [
            "언제나 뭔가를 입증해야한다고 느끼고 생각하시나요?",
            "나를 입증하기 위해 필요하지 않은 약속까지 하고 스스로를 괴롭히고 있지는 않은가요?"
        ]
        question = random.choice(qlist_3)
    elif ct == 4 and defined:
        qlist_3 = [
            "에고 센터 (정의) 비자아 질문"
        ]
        question = random.choice(qlist_3)

    # 방향센터
    elif ct == 5 and not defined:
        qlist_4 = [
            "본인은 끊임없이 사랑을 찾고 있는가요?",
            "본인은 지속적으로 삶의 의미와 방향성을 찾고 있는가?",
            "수시로 바뀌는 자신에게 늘 불안감을 느끼는가요?"
        ]
        question = random.choice(qlist_4)
    elif ct == 5 and defined:
        qlist_4 = [
            "방향 센터 (정의) 비자아 질문"
        ]
        question = random.choice(qlist_4)

    # 표현센터
    elif ct == 6 and not defined:
        qlist_5 = [
            "본인은 끊임없이 사랑을 찾고 있는가요?",
            "본인은 지속적으로 삶의 의미와 방향성을 찾고 있는가?",
            "수시로 바뀌는 자신에게 늘 불안감을 느끼는가요?"
        ]
        question = random.choice(qlist_5)
    elif ct == 6 and defined:
        qlist_5 = [
            "표현 센터 (정의) 비자아 질문"
        ]
        question = random.choice(qlist_5)
    question_intro = [
        "제가 질문 한가지 할게요! 질문을 보시고 솔직하게 답변해주시면 됩니다 :)",
        "지금까지 설명을 토대로 내담자님의 성향에 대해서 한가지 질문할게요!!",
        "잘 따라오고 계신가요? 내담자님의 성향을 파악하기 위해서 질문 하나 드릴게요 :)"
    ]
    q_intro = random.choice(question_intro)
    return [q_intro, question]

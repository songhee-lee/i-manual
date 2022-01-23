from transformers import BertTokenizer, BertForQuestionAnswering, AutoConfig
import torch
import pandas as pd
import random
from pymongo import MongoClient

# MongoDB setting
my_client = MongoClient("mongodb://localhost:27017/")
mydb = my_client['i-Manual']  # i-Manaul database 생성
mycol = mydb['users']  # users Collection 생성

model_path = "songhee/i-manual-mbert"
config = AutoConfig.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForQuestionAnswering.from_pretrained(model_path, config=config)

import pandas as pd

unego_description_csv = pd.read_csv("./data/자아_비자아 question.csv")
unego_description = []
for i in range(0, 93):
    unego_description.append(unego_description_csv.iloc[i, 1])

def extract_metadata_from_tracker(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']


def convert_ego_or_unego(i):
    if i==1:
        return "자아"
    elif i==-1:
        return "비자아"
    else:
        return "X"

def sentiment_get_ego_or_unego(ego_or_unego, metadata=None):
    # Mongo DB
    if metadata != None:
        ego_or_unego = list(map(convert_ego_or_unego, ego_or_unego))
        mycol.update({"displayID": metadata["uID"]}, { "$set" :{"self_notSelf": ego_or_unego}})

def unego_answer(question, user_text, metadata=None):
  if metadata != None:
    mycol.update({"displayID": metadata["uID"]}, { "$addToSet" :{"unego_answer" : {question :user_text}}})

def koelectra_qa_getanswer(context, question, metadata=None, qa_step=''):
    # Mongo DB 
    if qa_step:    # '종족' QA는 저장 안함
        if metadata != None:
            # add user question
            mycol.update({"displayID": metadata["uID"]}, {"$addToSet": { "question": {question:qa_step} }})

    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    answer_start_scores, answer_end_scores = model(**inputs, return_dict=False)
    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(
        answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    answer = remove_white_space(answer)
    
    return answer


def unego_get_question(ct, unego_count, defined=False):
    question = ""
    # 0: 연료, 1: 활력, 2: 직관, 3: 감정, 4: 에고, 5: 방향, 6: 표현, 7: 생각, 8: 영감
    # 연료센터
    if ct == 0 and not defined:
        qlist_0 = [
            unego_description[0],
            unego_description[1],
            unego_description[2]
        ]
        question = qlist_0[unego_count]
        ego_comment = unego_description[3]
        unego_comment = unego_description[4]

    elif ct == 0 and defined:
        qlist_0 = [
            unego_description[5],
            unego_description[6],
            unego_description[7]
        ]
        question = qlist_0[unego_count]
        ego_comment = unego_description[8]
        unego_comment = unego_description[9]
    # 활력센터
    elif ct == 1 and not defined:
        qlist_1 = [
            unego_description[10],
            unego_description[11],
            unego_description[12]
        ]
        question = qlist_1[unego_count]
        ego_comment = unego_description[13]
        unego_comment = unego_description[14]
    elif ct == 1 and defined:
        qlist_1 = [
            unego_description[15],
            unego_description[16],
            unego_description[17]
        ]
        question = qlist_1[unego_count]
        ego_comment = unego_description[18]
        unego_comment = unego_description[19]
    # 직관센터
    elif ct == 2 and not defined:
        qlist_2 = [
            unego_description[20],
            unego_description[21],
            unego_description[22]
        ]
        question = qlist_2[unego_count]
        ego_comment = unego_description[23]
        unego_comment = unego_description[24]

    elif ct == 2 and defined:
        qlist_2 = [
            unego_description[25],
            unego_description[26],
            unego_description[27]
        ]
        question = qlist_2[unego_count]
        ego_comment = unego_description[28]
        unego_comment = unego_description[29]

    # 감정센터
    elif ct == 3 and not defined:
        qlist_3 = [
            unego_description[30],
            unego_description[31],
            unego_description[32]
        ]
        question = qlist_3[unego_count]
        ego_comment = unego_description[33]
        unego_comment = unego_description[34]

    elif ct == 3 and defined:
        qlist_3 = [
            unego_description[35],
            unego_description[36],
            unego_description[37]
        ]
        question = qlist_3[unego_count]
        ego_comment = unego_description[38]
        unego_comment = unego_description[39]
    # 에고센터
    elif ct == 4 and not defined:
        qlist_4 = [
            unego_description[40],
            unego_description[41],
            unego_description[42]
        ]
        question = qlist_4[unego_count]
        ego_comment = unego_description[43]
        unego_comment = unego_description[44]

    elif ct == 4 and defined:
        qlist_4 = [
            unego_description[45],
            unego_description[46],
            unego_description[47]
        ]
        question = qlist_4[unego_count]
        ego_comment = unego_description[48]
        unego_comment = unego_description[49]

    # 방향센터
    elif ct == 5 and not defined:
        qlist_5 = [
            unego_description[50],
            unego_description[51],
            unego_description[52]
        ]
        question = qlist_5[unego_count]
        ego_comment = unego_description[53]
        unego_comment = unego_description[54]

    elif ct == 5 and defined:
        qlist_5 = [
            unego_description[55],
            unego_description[56],
            unego_description[57]
        ]
        question = qlist_5[unego_count]
        ego_comment = unego_description[58]
        unego_comment = unego_description[59]

    # 표현센터
    elif ct == 6 and not defined:
        qlist_6 = [
            unego_description[60],
            unego_description[61],
            unego_description[62]
        ]
        question = qlist_6[unego_count]
        ego_comment = unego_description[63]
        unego_comment = unego_description[64]

    elif ct == 6 and defined:
        qlist_6 = [
            unego_description[65],
            unego_description[66],
            unego_description[67]
        ]
        question = qlist_6[unego_count]
        ego_comment = unego_description[68]
        unego_comment = unego_description[69]

    # 생각센터
    elif ct == 7 and not defined:
        qlist_7 = [
            unego_description[70],
            unego_description[71],
            unego_description[72]
        ]
        question = qlist_7[unego_count]
        ego_comment = unego_description[73]
        unego_comment = unego_description[74]

    elif ct == 7 and defined:
        qlist_7 = [
            unego_description[75],
            unego_description[76],
            unego_description[77]
        ]
        question = qlist_7[unego_count]
        ego_comment = unego_description[78]
        unego_comment = unego_description[79]

    # 영감센터
    elif ct == 8 and not defined:
        qlist_8 = [
            unego_description[80],
            unego_description[81],
            unego_description[82]
        ]
        question = qlist_8[unego_count]
        ego_comment = unego_description[83]
        unego_comment = unego_description[84]

    elif ct == 8 and defined:
        qlist_8 = [
            unego_description[85],
            unego_description[86],
            unego_description[87]
        ]
        question = qlist_8[unego_count]
        ego_comment = unego_description[88]
        unego_comment = unego_description[89]

    return [question, ego_comment, unego_comment]

def remove_white_space(answer):

    if not answer:
        return answer

    # 작은 따옴표의 개수에 따라 시작 위치 변경
    toggle_c = answer.count("'")
    
    if toggle_c and toggle_c % 2 == 0 :  #짝수개일 경우 시작부분부터 시작  카운트
        toggle = True
    else :
        toggle = False      #홀수개일 경우 끝부분부터 시작 카운트
   
    tokens = answer.split()
    l_space = ["‘"]  # 다음 토큰에 붙어야 하는 토큰
    r_space = [",", ".","!","?",")", "~","%"] # 이전 토큰에 붙어야하는 토큰
    numbers = ["0", "1","2","3","4","5","6","7","8","9"]
    n_space = ["(","/","’"] # 앞뒤 토큰 모두 붙어야 하는 토큰
    length = len(tokens)

    result = []
    result.append(tokens[0])
    l_s = False
    for i in range(1, length):
         
        # 앞 뒤로 다 붙어야 하는 경우
        if tokens[i] in n_space:
            result[-1] = result[-1] + tokens[i]
            l_s = True
            continue
        
        if (tokens[i-1] =="~" or tokens[i-1]==".") and tokens[i][0] in numbers:
            result[-1] = result[-1] + tokens[i]
            continue

        if (tokens[i-1] == "'" and toggle) or (tokens[i-1]==")" and len(tokens[i])==1):
            result[-1] = result[-1] + tokens[i]
            continue
        
        # 다음 토큰에 붙어야 하는 경우
        if tokens[i] in l_space or (tokens[i] == "'" and toggle):
            l_s = True
            
            result.append(tokens[i])
            
            if tokens[i] == "'":
                toggle = False

            continue
        
        # 앞 토큰에 붙어야 하는 경우
        if (tokens[i] in r_space) or l_s or (tokens[i] == "'" and toggle==False):
            result[-1] = result[-1] + tokens[i]
            l_s = False

            if tokens[i] == "'":
                toggle = True
            
            continue
        
        result.append(tokens[i])
        

    return " ".join(result)

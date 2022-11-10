from transformers import BertTokenizer, BertForQuestionAnswering, AutoConfig, AutoTokenizer, AutoModelForQuestionAnswering
import torch
import pandas as pd
import random
from pymongo import MongoClient
import os
from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none
import scipy.io.wavfile
import shutil
import boto3
import sys
from actions.config import S3_CONFIG

# MongoDB setting
my_client = MongoClient("mongodb://localhost:27017/")
mydb = my_client['i-Manual']  # i-Manaul database 생성
mycol = mydb['users']  # users Collection 생성

# 모델 로딩
kor_model_path = "songhee/i-manual-mbert"
kor_config = AutoConfig.from_pretrained(kor_model_path)
kor_tokenizer = BertTokenizer.from_pretrained(kor_model_path)
kor_model = BertForQuestionAnswering.from_pretrained(kor_model_path, config=kor_config)

eng_model_path = "nuri/i-manual-longformer"
eng_config = AutoConfig.from_pretrained(eng_model_path)
eng_tokenizer = AutoTokenizer.from_pretrained(eng_model_path)
eng_model = AutoModelForQuestionAnswering.from_pretrained(eng_model_path, config=eng_config)

import pandas as pd

unego_description_csv = pd.read_csv("./data/자아_비자아 question.csv")
unego_description = []
unego_description.append(unego_description_csv['korean'].values.tolist())
unego_description.append(unego_description_csv['english'].values.tolist())
unego_description.append(unego_description_csv['voiceID'].values.tolist())



def extract_metadata_from_tracker(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']


def convert_ego_or_unego(i):
    if i == 1:
        return "자아"
    elif i == -1:
        return "비자아"
    else:
        return "X"


def sentiment_get_ego_or_unego(ego_or_unego, metadata=None):
    # Mongo DB
    if metadata != None:
        ego_or_unego = list(map(convert_ego_or_unego, ego_or_unego))
        mycol.update({"displayID": metadata["uID"]}, {"$set": {"self_notSelf": ego_or_unego}})


def unego_answer(question, user_text, metadata=None):
    if metadata != None:
        mycol.update({"displayID": metadata["uID"]}, {"$addToSet": {"unego_answer": {question: user_text}}})

def get_TTS(string, metadata, vID):
    members= ['','4_minjun', '5_bahn', '6_berry', '7_sewon', '3_winnie', '2_eden', '1_jaewon', '9_juhyung', '10_jiho', '8_taehun' ]
    model = members[int(metadata['member'])] # 멤버별 모델 선택
    lang = int(metadata['lang'])        
    if lang :   # 영어인 경우
            ninei += '_eng'

    lang = 'English' if lang else 'Korean' # 언어 0 한국어 1 영어
    uID = metadata['uID']     # user ID                           
    out = str(uID) + "/" + str(metadata['lang']) + "/" + str(metadata['member']) # output path

    # output path 없으면 생성 
    if not os.path.exists(out) :   
        os.makedirs(out)
    
    hf = "songhee/tts_"
    text2speech = Text2Speech.from_pretrained(
        hf + model
            )
                                                                        
    with torch.no_grad():
        wav = text2speech(string)["wav"]                                
    
    out_file_name = out+"/"+str(vID)+".wav"                                    
    scipy.io.wavfile.write(out_file_name, text2speech.fs , wav.view(-1).cpu().numpy())
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_CONFIG['accessKey'],
        aws_secret_access_key=S3_CONFIG['secretKey']
    )

    # out_file_name 그대로
    bucket_name = S3_CONFIG['bucket_name']
    s3.upload_file(out_file_name,bucket_name,"/chatbot/users/" + out + str(vID) + ".wav") 
    
    return "users/" + out_file_name 

def qa_getanswer(context, question, metadata=None, qa_step=''):
    # Mongo DB 
    if qa_step:  # '종족' QA는 저장 안함
        if metadata != None:
            # add user question
            mycol.update({"displayID": metadata["uID"]}, {"$addToSet": {"question": {question: qa_step}}})

    if metadata["lang"] == 0:
        inputs = kor_tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        answer_start_scores, answer_end_scores = kor_model(**inputs, return_dict=False)
        answer_start = torch.argmax(
            answer_start_scores
        )
        # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(
            answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
        answer = kor_tokenizer.convert_tokens_to_string(
            kor_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        answer = remove_white_space(answer)

    else:
        inputs = eng_tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        answer_start_scores, answer_end_scores = eng_model(**inputs, return_dict=False)
        answer_start = torch.argmax(
            answer_start_scores
        ) + 1
        # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(
            answer_end_scores) + 2  # Get the most likely end of answer with the argmax of the score
        answer = eng_tokenizer.convert_tokens_to_string(
            eng_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        answer = remove_white_space(answer)

    return answer


def unego_get_question(ct, unego_count, lang, defined=False):
    question = ""
    # 0: 연료, 1: 활력, 2: 직관, 3: 감정, 4: 에고, 5: 방향, 6: 표현, 7: 생각, 8: 영감
    # 연료센터
    vlist=[]
    if ct == 0 and not defined:
        qlist_0 = [
            unego_description[lang][0],
            unego_description[lang][1],
            unego_description[lang][2]
        ]
        question = qlist_0[unego_count]
        ego_comment = unego_description[lang][3]
        unego_comment = unego_description[lang][4]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"

    elif ct == 0 and defined:
        qlist_0 = [
            unego_description[lang][5],
            unego_description[lang][6],
            unego_description[lang][7]
        ]
        question = qlist_0[unego_count]
        ego_comment = unego_description[lang][8]
        unego_comment = unego_description[lang][9]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    # 활력센터
    elif ct == 1 and not defined:
        qlist_1 = [
            unego_description[lang][10],
            unego_description[lang][11],
            unego_description[lang][12]
        ]
        question = qlist_1[unego_count]
        ego_comment = unego_description[lang][13]
        unego_comment = unego_description[lang][14]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 1 and defined:
        qlist_1 = [
            unego_description[lang][15],
            unego_description[lang][16],
            unego_description[lang][17]
        ]
        question = qlist_1[unego_count]
        ego_comment = unego_description[lang][18]
        unego_comment = unego_description[lang][19]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    # 직관센터
    elif ct == 2 and not defined:
        qlist_2 = [
            unego_description[lang][20],
            unego_description[lang][21],
            unego_description[lang][22]
        ]
        question = qlist_2[unego_count]
        ego_comment = unego_description[lang][23]
        unego_comment = unego_description[lang][24]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 2 and defined:
        qlist_2 = [
            unego_description[lang][25],
            unego_description[lang][26],
            unego_description[lang][27]
        ]
        question = qlist_2[unego_count]
        ego_comment = unego_description[lang][28]
        unego_comment = unego_description[lang][29]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    # 감정센터
    elif ct == 3 and not defined:
        qlist_3 = [
            unego_description[lang][30],
            unego_description[lang][31],
            unego_description[lang][32]
        ]
        question = qlist_3[unego_count]
        ego_comment = unego_description[lang][33]
        unego_comment = unego_description[lang][34]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 3 and defined:
        qlist_3 = [
            unego_description[lang][35],
            unego_description[lang][36],
            unego_description[lang][37]
        ]
        question = qlist_3[unego_count]
        ego_comment = unego_description[lang][38]
        unego_comment = unego_description[lang][39]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    # 에고센터
    elif ct == 4 and not defined:
        qlist_4 = [
            unego_description[lang][40],
            unego_description[lang][41],
            unego_description[lang][42]
        ]
        question = qlist_4[unego_count]
        ego_comment = unego_description[lang][43]
        unego_comment = unego_description[lang][44]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 4 and defined:
        qlist_4 = [
            unego_description[lang][45],
            unego_description[lang][46],
            unego_description[lang][47]
        ]
        question = qlist_4[unego_count]
        ego_comment = unego_description[lang][48]
        unego_comment = unego_description[lang][49]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    # 방향센터
    elif ct == 5 and not defined:
        qlist_5 = [
            unego_description[lang][50],
            unego_description[lang][51],
            unego_description[lang][52]
        ]
        question = qlist_5[unego_count]
        ego_comment = unego_description[lang][53]
        unego_comment = unego_description[lang][54]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 5 and defined:
        qlist_5 = [
            unego_description[lang][55],
            unego_description[lang][56],
            unego_description[lang][57]
        ]
        question = qlist_5[unego_count]
        ego_comment = unego_description[lang][58]
        unego_comment = unego_description[lang][59]
        vlist = [
            "out_5/65601.wav",
            "out_5/65701.wav",
            "out_5/65801.wav"
        ]
        unego_voice = "out_5/66004.wav"
        unego_comment_voice = "out_5/66001.wav"
        ego_comment_voice = "out_5/65901.wav"
    # 표현센터
    elif ct == 6 and not defined:
        qlist_6 = [
            unego_description[lang][60],
            unego_description[lang][61],
            unego_description[lang][62]
        ]
        question = qlist_6[unego_count]
        ego_comment = unego_description[lang][63]
        unego_comment = unego_description[lang][64]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 6 and defined:
        qlist_6 = [
            unego_description[lang][65],
            unego_description[lang][66],
            unego_description[lang][67]
        ]
        question = qlist_6[unego_count]
        ego_comment = unego_description[lang][68]
        unego_comment = unego_description[lang][69]
        vlist = [
            "out_5/66601.wav",
            "out_5/66701.wav",
            "out_5/66801.wav"
        ]
        unego_voice = "out_5/67004.wav"
        unego_comment_voice = "out_5/67001.wav"
        ego_comment_voice = "out_5/66901.wav"
    # 생각센터
    elif ct == 7 and not defined:
        qlist_7 = [
            unego_description[lang][70],
            unego_description[lang][71],
            unego_description[lang][72]
        ]
        question = qlist_7[unego_count]
        ego_comment = unego_description[lang][73]
        unego_comment = unego_description[lang][74]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 7 and defined:
        qlist_7 = [
            unego_description[lang][75],
            unego_description[lang][76],
            unego_description[lang][77]
        ]
        question = qlist_7[unego_count]
        ego_comment = unego_description[lang][78]
        unego_comment = unego_description[lang][79]
        vlist = [
            "out_5/67601.wav",
            "out_5/67701.wav",
            "out_5/67801.wav"
        ]
        unego_voice = "out_5/68004.wav"
        unego_comment_voice = "out_5/68001.wav"
        ego_comment_voice = "out_5/67901.wav"
    # 영감센터
    elif ct == 8 and not defined:
        qlist_8 = [
            unego_description[lang][80],
            unego_description[lang][81],
            unego_description[lang][82]
        ]
        question = qlist_8[unego_count]
        ego_comment = unego_description[lang][83]
        unego_comment = unego_description[lang][84]
        vlist = [
            "out_5/.wav",
            "out_5/.wav",
            "out_5/.wav"
        ]
        unego_voice = "out_5/.wav"
        unego_comment_voice = "out_5/.wav"
        ego_comment_voice = "out_5/.wav"
    elif ct == 8 and defined:
        qlist_8 = [
            unego_description[lang][85],
            unego_description[lang][86],
            unego_description[lang][87]
        ]
        vlist = [
            "out_5/68601.wav",
            "out_5/68701.wav",
            "out_5/68801.wav"
        ]
        unego_voice = "out_5/69004.wav"
        unego_comment_voice = "out_5/69001.wav"
        ego_comment_voice = "out_5/68901.wav"
        question = qlist_8[unego_count]
        ego_comment = unego_description[lang][88]
        unego_comment = unego_description[lang][89]
    voice = vlist[unego_count]

    return [question, ego_comment, unego_comment, voice, unego_voice, unego_comment_voice, ego_comment_voice]


def remove_white_space(answer):
    if not answer:
        return answer

    # 작은 따옴표의 개수에 따라 시작 위치 변경
    toggle_c = answer.count("'")

    if toggle_c and toggle_c % 2 == 0:  # 짝수개일 경우 시작부분부터 시작  카운트
        toggle = True
    else:
        toggle = False  # 홀수개일 경우 끝부분부터 시작 카운트

    tokens = answer.split()
    l_space = ["‘"]  # 다음 토큰에 붙어야 하는 토큰
    r_space = [",", ".", "!", "?", ")", "~", "%"]  # 이전 토큰에 붙어야하는 토큰
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    n_space = ["(", "/", "’"]  # 앞뒤 토큰 모두 붙어야 하는 토큰
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

        if (tokens[i - 1] == "~" or tokens[i - 1] == ".") and tokens[i][0] in numbers:
            result[-1] = result[-1] + tokens[i]
            continue

        if (tokens[i - 1] == "'" and toggle) or (tokens[i - 1] == ")" and len(tokens[i]) == 1):
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
        if (tokens[i] in r_space) or l_s or (tokens[i] == "'" and toggle == False):
            result[-1] = result[-1] + tokens[i]
            l_s = False

            if tokens[i] == "'":
                toggle = True

            continue

        result.append(tokens[i])

    return " ".join(result)
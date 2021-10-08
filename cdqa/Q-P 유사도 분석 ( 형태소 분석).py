#!/usr/bin/env python
# coding: utf-8

# In[ ]:


json_file_name = 'i-manual-321006-6ae924a51dde.json'
tokenizer_dic_name = 'add_tok'


# # 1. Load Data

# In[ ]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)


#client_email = 'data-load@i-manual-321006.iam.gserviceaccount.com'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1s36W9DHgnN0fBgZRLjxZOPOdGo21xJByz6cvMiljA4A/edit#gid=301631691'

# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet1 = doc.worksheet('STRATEGY')
worksheet2 = doc.worksheet('AUTHORITY')
worksheet3 = doc.worksheet('TYPE')
worksheet4 = doc.worksheet('DEFINITION')
worksheet5 = doc.worksheet('CENTER')
worksheet6 = doc.worksheet('PROFILE')

from gspread_dataframe import get_as_dataframe, set_with_dataframe

df1 = get_as_dataframe(worksheet1)
df2 = get_as_dataframe(worksheet2)
df3 = get_as_dataframe(worksheet3)
df4 = get_as_dataframe(worksheet4)
df5 = get_as_dataframe(worksheet5)
df6 = get_as_dataframe(worksheet6)

df1 = df1[:53]
df2 = df2[:140]
df3 = df3[:37]
df4 = df4[:50]
df5 = df5[:102]
df6 = df6[:120]


# all_data : google spread sheet 에서 가져온 전체 데이터
# <br>anwers : 전체 데이터 중 'paragraph' 데이터
# <br>all_question_list : 전체 데이터 중 'question' 데이터

# In[ ]:


import pandas as pd 

all_data = pd.concat([df1,df2,df3,df4,df5,df6])
all_data['paragraph'] = all_data['paragraph'].fillna(method = 'ffill')
answers = all_data['paragraph'].tolist()

all_question_list = all_data['question'].tolist()


# ## tag 붙이기
# all_questions : 전체 question에 tag 붙이기
# <br>all_answers : question에 대한 paragraph

# In[ ]:


def concat_tag(name, title ,question):
    if name != '':
        return name + " : " + question
    else:
        return title + " : " + str(question)


# In[ ]:


def concat_tag_answer(name, title, answer):
    if name != '':
        return name + " - " + title + " : " + answer
    else:
        return title + " : " + answer


# In[ ]:


#Question & Answer 뽑아내기
all_questions = {}
all_answers = {}
all_qa_answers = {}

df_list = [df1, df2, df3, df4, df5, df6]
df_name = ['전략', '결정 방식', '종족', '에너지 흐름','','사회적 성향']

for df, name in zip(df_list, df_name):
    df['제목'] = df['제목'].fillna('')
    df['paragraph_'] = df['paragraph'].fillna(method='ffill')

    title = df['제목']
    q = df['question']
    a = df['paragraph_']
    qa_ans = df['answer'].tolist()
    
    questions = []
    answers_ = []
    qa_answers = []
    
    for i in range(0, len(df)):
        if title[i] != '':
            if questions:
                all_questions[t] = questions
                questions = []
                questions.append( concat_tag(name, title[i], q[i]) )
            else:
                all_questions[title[i]] = []
                questions.append( concat_tag(name, title[i], q[i]) )
                
            if answers_ :
                all_answers[t] = answers_
                answers_ = []
                answers_.append(concat_tag_answer(name, title[i], a[i]))
            else:
                all_answers[title[i]] = []
                answers_.append(concat_tag_answer(name, title[i], a[i]))
            
            if qa_answers:
                all_qa_answers[t] = qa_answers
                qa_answers = []
                qa_answers.append(qa_ans[i])
            else:
                all_qa_answers[title[i]] = []
                qa_answers.append(qa_ans[i])
            
            t = title[i]
        else:
            questions.append( concat_tag(name, t, q[i]) )
            answers_.append( concat_tag_answer(name, t, a[i]))
            qa_answers.append(qa_ans[i])
                                  
    all_questions[t] = questions
    all_answers[t] = answers_
    all_qa_answers[t] = qa_answers


# In[ ]:


#all_qa_answers


# ## i-Manual 통합 버전 데이터 정제

# In[ ]:


# I-manual 통합 버전
import pandas as pd
import numpy as np
df = pd.concat([df1,df2,df3,df4,df5,df6])
df_new = df.drop(['내용','answer_start_pos','id', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9',
       'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13',
       'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17',
       'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21',
       'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25'], axis=1)
df = df.drop(['내용', 'answer','answer_start_pos','question','id', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9',
       'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13',
       'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17',
       'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21',
       'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25'], axis=1)

df = df.dropna()
df = df.reset_index()
df = df.replace('', np.NaN)
df = df.fillna(method='ffill')


# In[ ]:


#df


# ### 전체 데이터 tag

# In[ ]:


all_tags = list(dict.fromkeys(df['제목'].tolist()))

all_paragraph_tags = []
for i in range(0, len(all_tags)):
    if i < 5:
        all_paragraph_tags.append("전략 - "+all_tags[i])
    elif i < 13 :
        all_paragraph_tags.append("결정 방식 - "+all_tags[i])
    elif i < 18:
        all_paragraph_tags.append("종족 - "+all_tags[i])
    elif i < 23:
        all_paragraph_tags.append("에너지 흐름 - "+all_tags[i])
    elif 40 < i :
        all_paragraph_tags.append("사회적 성향 - "+all_tags[i])
    else :
        all_paragraph_tags.append(all_tags[i])
        


# In[ ]:


all_paragraphs = []
for tag, tag_ in zip(all_tags, all_paragraph_tags):
    index = df.index[df['제목']==tag].tolist()
    for i in index:
        all_paragraphs.append(tag_+" : "+df.loc[i, 'paragraph'])


# ### 내담자 tag (예시) 

# In[ ]:


tags = ['가이드', 
       '은둔자/은근 사교가 (2/4)', 
       '두 묶음 흐름', 
       '감정 결정방식', 
       '가이드의 전략',
       '연료센터(DEFINED)',      
       '활력센터(UNDEFINED)',
       '직관센터(UNDEFINED)',
       '감정센터(DEFINED)',
       '에고센터(DEFINED)',
       '방향센터(UNDEFINED)',
       '생각센터(DEFINED)',
       '영감센터(DEFINED)',
       '표현센터(DEFINED)'
      ]

paragraph_tags = ['종족 - 가이드', 
       '사회적 성향 - 은둔자/은근 사교가(2/4)', 
       '에너지 흐름 - 두 묶음 흐름', 
       '결정 방식 - 감정 결정방식', 
       '전략 - 가이드의 전략',
       '연료센터(DEFINED)',      
       '활력센터(UNDEFINED)',
       '직관센터(UNDEFINED)',
       '감정센터(DEFINED)',
       '에고센터(DEFINED)',
       '방향센터(UNDEFINED)',
       '생각센터(DEFINED)',
       '영감센터(DEFINED)',
       '표현센터(DEFINED)'
      ]


# ## 내담자별 정보 추출

# ### CONTEXT - 내담자의 정보 리스트 (Paragraph)

# In[ ]:


paragraphs = []
for tag, tag_ in zip(tags, paragraph_tags):
    index = df.index[df['제목']==tag].tolist()
    for i in index:
        paragraphs.append(tag_+" : "+df.loc[i, 'paragraph'])


# In[ ]:


len(paragraphs)


# In[ ]:


#paragraphs


# ### Question - 내담자의 정보에 대한 질문 리스트

# In[ ]:


personal_questions = {}
for tag in tags:
    personal_questions[tag] = all_questions[tag]


# In[ ]:


#personal_questions


# ### Answer - 내담자의 정보에 대한 정답 리스트

# In[ ]:


personal_answers = {}
for tag in tags:
    personal_answers[tag] = all_answers[tag]


# In[ ]:


#personal_answers


# ### QA Answer - 내담자 정보에 대한 QA 정답 리스트

# In[ ]:


personal_qa_answers = {}
for tag in tags:
    personal_qa_answers[tag] = all_qa_answers[tag]


# In[ ]:


#personal_qa_answers


# # 2. Tokenizer
# 직접 학습시킨 tokenizer 사용

# In[ ]:


from transformers import BertTokenizer
#tokenizer = BertTokenizer.from_pretrained('songhee/i-manual-mbert')
tokenizer = BertTokenizer.from_pretrained(tokenizer_dic_name)


# ### tokenizer

# In[ ]:


def my_tokenizer(text):
    inputs = tokenizer(text, add_special_tokens=False, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    return text_tokens


# ### 불용어 제거

# In[ ]:


def remove_words(stop_words, text_list):
    """불용어 제거"""
    stop_words = stop_words.split(' ')
    
    # merge morphs to words
    edit = []
    
    for text in text_list:
        tmp = []
        for token in text:
            if token not in stop_words:
                tmp.append(token)

        edit.append(tmp)

    return edit


# ### 단어로 합치기(##제거)

# In[ ]:


def merge_morphs(text_list):
    """
    단어로 합치기(##제거)
    """
    edit = []
    
    for text in text_list:
        tmp = []
        for i in range (0, len(text)) :
            if text[i][:2] == '##' :
                a = []
                a.append(tmp[-1])
                a.append(text[i][2:])
                tmp[-1] = ''.join(a)
            else :
                tmp.append(text[i])

        edit.append(tmp)
    
    return edit


# ### paragraph tokenize 함수
# 1. text 토큰화
# 2. 토큰화된 상태에서 불용어 제거 (morphs)
# 3. 토큰화된 상태를 단어로 합치기
# 4. 단어 상태의 불용어 제거 (words)
# 5. 분리된 단어를 문장으로 합치기

# In[ ]:


def tokenized_text(text_list):
    
    # tokenized paragraphs
    tokenized_paragraphs = []

    for text in text_list:
        tokenized_paragraphs.append(my_tokenizer(text))
    
    # remove stop words(morphs)
    stop_words = '##은 ##을 ##를 ##에 ##의 ##이 ##으로 ##로 ##에게 ##것' ###입 ##니다 ##습 ##합
    tokenized_paragraphs_edit = remove_words(stop_words, tokenized_paragraphs)
    
    # merge morphs to words
    tokenized_paragraphs_edit = merge_morphs(tokenized_paragraphs_edit)
    #tokenized_paragraphs_edit = merge_morphs(tokenized_paragraphs)
    
    # remove stop words(words)
    stop_words = "입니다 합니다 있습니다 또한 것입니다 그리고 또는 것이 것을 의 ' : ? ! !! ?' !' , . #" + '"'
    tokenized_paragraphs_edit = remove_words(stop_words, tokenized_paragraphs_edit)
    
    return tokenized_paragraphs_edit


# ### Tokenize paragraph + 역토큰화

# In[ ]:


tokenized_corpus = tokenized_text(paragraphs)


# In[ ]:


def detokenized(tokenized_corpus):
    # merge words to sentences
    """분리된 단어를 문장으로 합치기"""
    tokenized_paragraphs = []
    stop_words = "입니다 합니다 있습니다 또한 것입니다 그리고 또는 것이 것을 의 ' : ? ! !! ?' !' , . #" + '"'

    for i in range(0, len(tokenized_corpus)):
        sentence = ""
        for w in tokenized_corpus[i] :
            if w not in stop_words :
                sentence += w
                sentence += " "
        tokenized_paragraphs.append(sentence)
    return tokenized_paragraphs


# In[ ]:


tokenized_paragraphs = detokenized(tokenized_corpus)


# ### 띄어쓰기 보정

# In[ ]:


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


# In[ ]:


tokenized_paragraphs_edit = []
for text in tokenized_paragraphs:
    tokenized_paragraphs_edit.append(remove_white_space(text))


# ### 전체 데이터에 대한 paragraph

# In[ ]:


all_tokenized_corpus = tokenized_text(all_paragraphs)
# 역 토큰화
all_tokenized_paragraphs = detokenized(all_tokenized_corpus)


# In[ ]:


all_tokenized_paragraphs_edit = []
for text in all_tokenized_paragraphs:
    all_tokenized_paragraphs_edit.append(remove_white_space(text))


# In[ ]:


#all_tokenized_paragraphs_edit


# # 3. TF-IDF

# ### 유사도 구하는 함수

# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer

def get_similar_paragraphs(context, question, top_n=3, original_context=None):
    """
    context : 내담자의 전체 paragraphs를 토큰화한 결과
    original_context : 내담자의 전체 paragraphs (원본)
    question : 내담자 질문
    top_n : 1~n위의 유사도 결과 추출
    """
    
    if original_context is None:
        original = context
    else:
        original = original_context
    
    tfidf_vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(context+[question])
    doc_similarities = (tfidf_matrix * tfidf_matrix.T)
    
    #top_similar = similarities.argsort()[-(top_n+1):][::-1][1:]
    question_similarities = doc_similarities.toarray()[-1][:-1]
    top_similar = question_similarities.argsort()[::-1]
    
    output = {
            "question" : question,
            "top_similar_paragraphs": [{
                    "paragraphs": context[similar_idx],
                    "original_paragraphs" : original[similar_idx],
                    "similarity": round(question_similarities[similar_idx], 6)
            } for similar_idx in top_similar]
        }
    
    return output   


# In[ ]:





# # 형태소 분석 (무현 실험 분담)

# In[ ]:


from konlpy.tag import Mecab

def mecab_normalize(text_list):
    ###################################################################
    # 실질 형태소 품사
    meaning_tags = ["NNG", "NNP", "NNB", "NR", "NP", "VV", "VA", "VX", "VCP", "VCN", "MM", "MAG", "MAJ", "IC"]
    
    # 실질 형태소 + 어근, 접미사, 접두사
    meaning_tags = ["NNG", "NNP", "NNB", "NR", "NP", "VV", "VA", "VX", "VCP", "VCN", "MM", "MAG", "MAJ", "IC", "XR", "XPN", "XSN", "XSV", "XSA"]
    
    ########### 둘중 원하는 방식으로 사용하면 됩니다. ##################
    
    # 딕셔너리 파일 위치는 사용자 별로 상이
    m = Mecab('C:\\mecab\\mecab-ko-dic')
    
    meaning_text = []
    for text in text_list:
        out = m.pos(text)

        # 실질 형태소만 담는 배열
        meaning_words = []

        for word in out:
            # word의 형태는 ("단어", "품사") 이므로 word[1]은 품사를 나타내고 word[0]는 단어를 나타냄.
            if word[1] in meaning_tags:
                meaning_words.append(word[0])
        meaning_text.append(meaning_words)
    return meaning_text


# ## 4-1 내담자 Paragraphs

# In[ ]:


type_num = 1 # question만 형태소 분석
type_num = 2 # paragraphs만 형태소 분석
type_num = 3 # question과 paragraphs 형태소 분석


# In[ ]:


### paragraph
if type_num == 1:
    context = tokenized_paragraphs_edit
else:
    context = mecab_normalize(paragraphs)
    context = detokenized(paragraphs)
    context = [remove_white_space(text) for text in context]
    
correct = 0
incorrect = 0
a_c = 0
a_i = 0
result_dic = {'tag':[], '정답':[], '오답':[]}

for tag in tags:
    print("\n============",tag,"==============\n")
    
    ### question
    if type_num == 2:
        tokenized_questions = tokenized_text(personal_questions[tag])
    else :
        tokenized_questions = mecab_normalize(personal_questions[tag])
    tokenized_questions = detokenized(tokenized_questions)
   
    ### answer (original paragraph)
    answer_list = personal_answers[tag]
    if type_num == 1:
        answer_list = tokenized_text(answer_list)
    else:
        answer_list = mecab_normalize(answer_list)
    answer_list = detokenized(answer_list)
    answer_list = [ remove_white_space(text) for text in answer_list]
   
    ### TF-IDF
    for answer, question in zip(answer_list, tokenized_questions) :
        results = get_similar_paragraphs(context, question, 1)

        print(results['question'], "\n")

        if results['top_similar_paragraphs'][0]['similarity'] > 0 :
            prediction = results['top_similar_paragraphs'][0]['paragraphs']

            print(prediction, "\n")
            print(answer, "\n")

            if prediction == answer :
                correct +=1 
                print("==================================정답!\n")
            else :
                incorrect +=1
                print("==================================오답!\n")

    result_dic['tag'].append(tag)
    result_dic['정답'].append(correct)
    result_dic['오답'].append(incorrect)
    
    a_c += correct
    a_i += incorrect
    
    correct =0
    incorrect=0
    
result_df = pd.DataFrame(result_dic, columns=['tag','정답','오답'])


# In[ ]:


result_df


# In[ ]:





# ## 4-2 내담자 종족, 결정 방식

# In[ ]:


type_num = 1 # question만 형태소 분석
type_num = 2 # paragraphs만 형태소 분석
type_num = 3 # question과 paragraphs 형태소 분석


# In[ ]:


### paragraph
if type_num == 1:
    context = tokenized_paragraphs_edit
else:
    context = mecab_normalize(paragraphs)
    context = detokenized(paragraphs)
    context = [remove_white_space(text) for text in context]

setting = [['가이드', 0,2], ['감정 결정방식',4,6]]
for tag, start, end in setting :
    print("\n============",tag,"==============\n")
    c = context[start:end]
    
    correct = 0
    incorrect = 0

    ### question
    if type_num == 2:
        tokenized_questions = tokenized_text(personal_questions[tag])
    else :
        tokenized_questions = mecab_normalize(personal_questions[tag])
    tokenized_questions = detokenized(tokenized_questions)
   
    ### answer (original paragraph)
    answer_list = personal_answers[tag]
    if type_num == 1:
        answer_list = tokenized_text(answer_list)
    else:
        answer_list = mecab_normalize(answer_list)
    answer_list = detokenized(answer_list)
    answer_list = [ remove_white_space(text) for text in answer_list]
    
    # TF-IDF
    for answer, question in zip(answer_list, tokenized_questions) :
        results = get_similar_paragraphs(c, question, top_n)

        print(results['question'], "\n")

        if results['top_similar_paragraphs'][0]['similarity'] > 0 :
            prediction = results['top_similar_paragraphs'][i]['paragraphs'].replace(tag_+ " : ", '')
            prediction = results['top_similar_paragraphs'][0]['paragraphs']

            print(prediction, "\n")
            print(answer, "\n")

            if prediction == answer :
                correct +=1 
                print("==================================정답!\n")
            else :
                incorrect +=1
                print("==================================오답!\n")
                
    print("---------result---------\n")
    print("정답: ",correct)
    print("오답: ",incorrect)


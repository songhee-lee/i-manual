import pandas as pd
import tag
from i-manual_tokenize import tokenized_text, detokenized, remove_white_space_text
from tf-idf import get_similar_paragraphs
from ../qatest import QuestionAnswering


# Load data
all_data = pd.read_csv('../data/i-Manual_data.csv') # 전체 데이터
all_data['paragraph'] = all_data['paragraph'].fillna(method = 'ffill')
answers = all_data['paragraph'].tolist() 
all_question_list = all_data['question'].tolist()

# Concate tag
##### get tag data from RASA
t = tag.tags(all_data, tags, paragraph_tags)

all_questions, all_answers, all_qa_answers = t.concat_tag_basic()
all_paragraphs = t.concat_tag_all()
paragraphs, personal_questions, personal_answers, personal_qa_answers = t.concat_tag_person()


# Tokenize
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('songhee/i-manual-mbert')
tokenized_corpus = tokenized_text(paragraphs)
tokenized_paragraphs = detokenized(tokenized_corpus)
tokenized_paragraphs_edit = remove_white_space_text(tokenized_paragraphs)


# TF-IDF
######## title, 사용자 질문 받아오기<리스트 형태> (현재 진행단계)
######## title에 대한 tag, context, paragraph 정하기
qa_module = QuestionAnswering('songhee/i-manual-mbert')

tokenized_question = tokenized_text(사용자 질문)
tokenized_question = detokenized(tokenized_question)

results = get_similar_paragraphs( 정해진 context, tokenized_question, 1, 실제 paragraph)  
if results['top_similar_paragraphs'][i]['similarity'] > 0 :
     context_ = results['top_similar_paragraphs'][i]['original_paragraphs'].replace(tag_+ " : ", '')
     prediction = qa_module(question_, context_ )

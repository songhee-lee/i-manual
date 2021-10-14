import pandas as pd
import numpy as np

def concat_tag(name, title ,question):
    if name != '':
        return name + " : " + question
    else:
        return title + " : " + str(question)
      
def concat_tag_answer(name, title, answer):
    if name != '':
        return name + " - " + title + " : " + answer
    else:
        return title + " : " + answer    

class tags(all_data, tags, paragraph_tags):
    self.all_data = all_data
    self.tags = tags
    self.paragraph_tags = paragraph_tags
    
    def concat_tag_basic():

      #Question & Answer 뽑아내기
      all_questions = {}
      all_answers = {}
      all_qa_answers = {}

      df_cut = [53, 193, 230, 280, 382]
      df_name = ['전략', '결정 방식', '종족', '에너지 흐름','','사회적 성향']

      all_data['제목'] = all_data['제목'].fillna('')
      all_data['paragraph_'] = all_data['paragraph'].fillna(method='ffill')

      title = all_data['제목'].tolist()
      q = all_data['question'].tolist()
      a = all_data['paragraph_'].tolist()
      qa_ans = all_data['answer'].tolist()

      questions = []
      answers_ = []
      qa_answers = []

      for i in range(0, len(all_data)):

          if i < df_cut[0]:
              name = df_name[0]
          elif i < df_cut[1]:
              name = df_name[1]
          elif i < df_cut[2]:
              name = df_name[2]
          elif i < df_cut[3]:
              name = df_name[3]
          elif i < df_cut[4]:
              name = df_name[4]
          else :
              name = df_name[5]


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

      return all_questions, all_answers, all_qa_answers

    def concat_tag_all():
      df = self.all_data.drop(['내용', 'answer','answer_start_pos','question','id', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9',
           'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13',
           'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17',
           'Unnamed: 18', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21',
           'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24', 'Unnamed: 25'], axis=1)
      df = df.dropna()
      df = df.reset_index()
      df = df.replace('', np.NaN)
      df = df.fillna(method='ffill')

      self.all_tags = list(dict.fromkeys(df['제목'].tolist()))
      self.all_paragraphs_tags = []
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

      all_paragraphs = []
      for tag, tag_ in zip(all_tags, all_paragraph_tags):
          index = df.index[df['제목']==tag].tolist()
          for i in index:
              all_paragraphs.append(tag_+" : "+df.loc[i, 'paragraph'])

      return all_paragraphs

    def concat_tag_person():
      # CONTEXT - 내담자의 정보 리스트 (paragraph)
      paragraphs = []
      df = self.all_data
      for tag, tag_ in zip(self.tags, self.paragraph_tags):
        index = df.index[df['제목']==tag].tolist()
        for i in index:
            paragraphs.append(tag_+" : "+df.loc[i, 'paragraph'])  
        
      # Question - 내담자의 정보에 대한 질문 리스트
      personal_questions = {}
        for tag in self.tags:
            personal_questions[tag] = all_questions[tag]
            
      # Answer - 내담자의 정보에 대한 정답 리스트
      personal_answers = {}
        for tag in self.tags:
            personal_answers[tag] = all_answers[tag]
      
      # QA Answer - 내담자 정보에 대한 QA 정답 리스트
      personal_qa_answers = {}
        for tag in self.tags:
            personal_qa_answers[tag] = all_qa_answers[tag]
      
      return paragraphs, personal_questions, personal_answers, personal_qa_answers
      

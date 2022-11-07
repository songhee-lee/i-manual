import pandas as pd
import torch
import torch.nn as nn
import numpy as np
from transformers import AutoTokenizer, ElectraForSequenceClassification, AdamW


# GPU 사용
device = torch.device("cpu")

#한국어 버전
kor_model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-small-v2-discriminator", num_labels = 3)
#model = nn.DataParallel(model) # use multi-gpu
kor_model.to(device)
kor_saved_checkpoint = torch.load("../data/model_ego_survey3.pt", map_location=torch.device('cpu'))
kor_model.load_state_dict(kor_saved_checkpoint, strict=False)
kor_tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-small-v2-discriminator")

#영어 버전
eng_model = ElectraForSequenceClassification.from_pretrained("google/electra-small-discriminator", num_labels = 3)
eng_model.to(device)
eng_saved_checkpoint = torch.load("../data/SA_eng_20.pt", map_location=torch.device('cpu'))
eng_model.load_state_dict(eng_saved_checkpoint, strict=False)
eng_tokenizer = AutoTokenizer.from_pretrained("google/electra-small-discriminator")

def convert_input_data(sentences, lang):

    if lang == 0: # Korean
        # Koelectra의 토크나이저로 문장을 토큰으로 분리
        tokenized_texts = [kor_tokenizer.tokenize(sent) for sent in sentences]

        # 입력 토큰의 최대 시퀀스 길이
        MAX_LEN = 128

        # 토큰을 숫자 인덱스로 변환
        input_ids = [kor_tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
         # 어텐션 마스크 초기화
        attention_masks = []

        # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
        # 패딩 부분은 electra 모델에서 어텐션을 수행하지 않아 속도 향상
        for seq in input_ids:
            seq_mask = [float(i > 0) for i in seq]
            attention_masks.append(seq_mask)

        # 데이터를 파이토치의 텐서로 변환

        inputs = torch.tensor(input_ids)
        masks = torch.tensor(attention_masks)
        return inputs, masks

    elif lang == 1:
        tokenized_texts = [eng_tokenizer.tokenize(sent) for sent in sentences]
        MAX_LEN = 128
        input_ids = [eng_tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]

        attention_masks = []
        for seq in input_ids:
            seq_mask = [float(i > 0) for i in seq]
            attention_masks.append(seq_mask)

        inputs = torch.tensor(input_ids)
        masks = torch.tensor(attention_masks)
        return inputs, masks


# 문장 테스트
def sentiment_predict(question, answer, lang):
    sentence = [question + ' ' + answer]

    # 문장을 입력 데이터로 변환
    inputs, masks = convert_input_data(sentence, lang)

    # 데이터를 GPU에 넣음
    b_input_ids = inputs.to(device)
    b_input_mask = masks.to(device)

    # 그래디언트 계산 안함
    with torch.no_grad():
        # Forward 수행
        if lang == 0: #Korean
            outputs = kor_model(b_input_ids,
                            token_type_ids=None,
                            attention_mask=b_input_mask)
            # 로스 구함
            logits = outputs[0]

            # CPU로 데이터 이동
            logits = logits.detach().cpu().numpy()
            result = np.argmax(logits)
            print(logits)
            # 0: 중립 1: 긍정 2: 부정
            return result

        elif lang == 1: # English
            outputs = eng_model(b_input_ids,
                            token_type_ids=None,
                            attention_mask=b_input_mask)
            
            logits = outputs[0]

            logits = logits.detach().cpu().numpy()
            result = np.argmax(logits)
            return result

    
if __name__ =="__main__":
    print(sentiment_predict("Have you ever regretted speaking up when you shouldn't have?", "yes i do!", 1)) # 1
    print(sentiment_predict("Do you feel exhausted after talking to someone or giving a presentation?", "no i don't!!", 1)) # 2
    print(sentiment_predict("Do you tend to make large hand or body movements when speaking?", "I don't know well...", 1)) # 0
    print(sentiment_predict("나는 취향이 확고한 편인가요?", "그런 편이에요", 0)) # 0
    print(sentiment_predict("무언가를 이해하려 끝없이 생각하며 스트레스를 받는 편인가요?", "그런 편이에요", 0)) # 0
    print(sentiment_predict("나는 주변에 의해 생각이 자주 바뀌는 편인가요?", "맞아요! 그런 것 같아요 ㅎㅎ", 0)) # 0





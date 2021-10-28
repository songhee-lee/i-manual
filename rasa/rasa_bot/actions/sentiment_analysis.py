import pandas as pd
import torch
import torch.nn as nn
import numpy as np
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, ElectraForSequenceClassification, AdamW
from tqdm.notebook import tqdm

# GPU 사용
device = torch.device("cpu")

model = ElectraForSequenceClassification.from_pretrained("monologg/koelectra-small-v2-discriminator", num_labels = 3)
model = nn.DataParallel(model) # use multi-gpu
model.to(device)
saved_checkpoint = torch.load("./data/model.pt", map_location=torch.device('cpu'))
model.load_state_dict(saved_checkpoint, strict=False)


def convert_input_data(sentences):
    # Koelectra의 토크나이저로 문장을 토큰으로 분리
    tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-small-v2-discriminator")
    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

    # 입력 토큰의 최대 시퀀스 길이
    MAX_LEN = 128

    # 토큰을 숫자 인덱스로 변환
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]

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


# 문장 테스트
def sentiment_predict(question, answer):
    sentence = [question + ' ' + answer]

    # 문장을 입력 데이터로 변환
    inputs, masks = convert_input_data(sentence)

    # 데이터를 GPU에 넣음
    b_input_ids = inputs.to(device)
    b_input_mask = masks.to(device)

    # 그래디언트 계산 안함
    with torch.no_grad():
        # Forward 수행
        outputs = model(b_input_ids,
                        token_type_ids=None,
                        attention_mask=b_input_mask)

    # 로스 구함
    logits = outputs[0]

    # CPU로 데이터 이동
    logits = logits.detach().cpu().numpy()
    result = np.argmax(logits)
    # 0: 중립 1: 긍정 2: 부정
    return result






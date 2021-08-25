# i-manual
- Finetune with i-manual test data
- Models
  - mBERT (bert-base-multilingual-cased)

<br><br>
## How to use
- Transformers 라이브러리에서 사용 가능
```python
from transformers import BertModel, BertTokenizer

model = BertModel.from_pretrained('songhee/i-manaul-mbert')
tokenizer = BertTokenizer.from_pretrained('songhee/i-manaul-mbert')
```

<br><br>
## Usage

- 코드는 monologg/KoBERT-KorQuAD 의 run_squad 를 가져와 일부 수정해 사용
- transformers 버전 변경으로 pretrained_config_archive_map.keys()를 그대로 사용할 수 없음.

<br><br>
### 1. Training

```bash
python3  run_squad.py  --model_type bert \
                       --model_name_or_path bert-base-multilingual-cased \
                       --output_dir {$output_dir} \
                       --data_dir {$data_dir} \
                       --train_file i-manual_train.json \
                       --per_gpu_train_batch_size 8 \
                       --per_gpu_eval_batch_size 8 \
                       --max_seq_length 512 \
		       --max_query_length 100 \
		       --max_answer_length 512 \
                       --logging_steps 100 \
                       --save_steps 100 \
                       --do_train \
```

### 2. Evaluation
- make prediction files

```bash
python  run_squad.py   --model_type bert \
                       --model_name_or_path {$trained_model_dir} \
                       --output_dir {$output_dir} \
                       --data_dir {$data_dir} \
                       --predict_file KorQuAD_v1.0_dev.json \
                       --per_gpu_train_batch_size 8 \
                       --per_gpu_eval_batch_size 8 \
                       --logging_steps 100 \
                       --save_steps 100 \
                       --do_eval \
```

- evaluate
```console
$ python3 evaluate_v1_0.py {$data_dir}/KorQuAD_v1.0_dev.json {$output_dir}/predictions_.json
```

<br><br>
## Results
1. i-maunal test data로 학습, i-manual test data로 테스트한 결과
2. i-manual test data를 train/dev 로 나누어 테스트한 결과

|                         | Exact Match (%) | F1 Score (%) |
| ----------------------- | --------------- | ------------ |
| mBERT (i-manual test)   |     99.79424    |   99.867896  |
| mBERT (i-manual dev)    |                 |              |


<br><br>

### i-manual data 변형
- 각 answer에 매칭되는 question 을 변형해 데이터 생성
- 1. 기존 question과 동일한 의미를 갖도록 변형
- 2. 해당 answer를 답변으로 할 만한 새로운 question 생성

```bash
$ python3 qatest_changed.py --model_name_or_path {$trained_model_dir} --data_path {$data_path}
```

|                         |      개수 (%)    | 
| ----------------------- | --------------- | 
| 동일한 답변/Good case      |        24       |
| White Space.            |        39       |
| [UNK]토큰 발생            |        30       |
| No answer.              |        5        |
| 다른 답변 중 Bad case      |        2        |

- white space는 원문 text 와 띄어쓰기의 차이가 있는 경우로 추후 보정하거나 보정하지 않아도 큰 문제가 아님
	-> <b>Remove white space 과정에서 해결 가능</b>
- [UNK] 토큰 발생은 토크나이저에 해당 vocab이 없는 경우로, <b>add vocab 과정에서 해결 가능</b>
- No answer는 답이 출력되지 않은 경우
- Bad case는 다른 답변을 출력했으나 답이 맞지 않다고 판단된 경우

<br><br>

## Add vocab
```bash
$ python3 python add_tokens.py --model_name_or_path {$trained_model_dir} --output_dir {$output_dir} --data_path {$data_dir}/add_tokens.txt
```
- add_tokens.txt : [UNK]를 출력하는 모든 token list.
- add_tokens.py : token list 파일을 입력할 때 trained_model에 token을 추가하고 다시 저장하는 함수
<br><br>
	
## Remove white space
- qatest.py 에 remove_white_space 함수 추가
- 앞 토큰에 붙어야 하는 경우, 뒷 토큰에 붙어야 하는 경우, 그리고 앞/뒤 토큰 모두 붙어야 하는 경우로 나누어 조건 생성
- 특수한 경우에 대한 조건 생성
<br> ex) 0.5% : 숫자와 기호는 붙여야 함
<br> ex) '아하!'(긍정) 소리는 <b>vs</b> 에너지(활력)가 있는지 : 경우에 따라 붙이고 띄어야 하는게 다른 경우
<br><br>	
## References

- [KoBERT-KorQuAD](https://github.com/monologg/KoBERT-KorQuAD)

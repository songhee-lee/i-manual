# i-manual
- Finetune with i-manual test data
- Models
  - mBERT (bert-base-multilingual-uncased)

## How to use
- Transformers 라이브러리에서 사용 가능
```python
from transformers import BertModel, BertTokenizer

model = BertModel.from_pretrained('songhee/i-manaul-mbert')
tokenizer = BertTokenizer.from_pretrained('songhee/i-manaul-mbert')
```

## Usage

- 코드는 monologg/KoBERT-KorQuAD 의 run_squad 를 가져와 일부 수정해 사용
- transformers 버전 변경으로 pretrained_config_archive_map.keys()를 그대로 사용할 수 없음.

### 1. Training

```bash
python  run_squad.py   --model_type bert \
                       --model_name_or_path bert-base-multilingual-uncased \
                       --output_dir {$output_dir} \
                       --data_dir {$data_dir} \
                       --train_file i-manual_train.json \
                       --predict_file KorQuAD_v1.0_dev.json \
                       --evaluate_during_training \
                       --per_gpu_train_batch_size 8 \
                       --per_gpu_eval_batch_size 8 \
                       --max_seq_length 512 \
                       --logging_steps 1000 \
                       --save_steps 4000 \
                       --do_train \
```


### 2. Evaluation
- make prediction files
```bash
python  run_squad.py   --model_type bert \
                       --model_name_or_path bert-base-multilingual-uncased \
                       --output_dir {$output_dir} \
                       --data_dir {$data_dir} \
                       --train_file i-manual_train.json \
                       --predict_file KorQuAD_v1.0_dev.json \
                       --per_gpu_train_batch_size 8 \
                       --per_gpu_eval_batch_size 8 \
                       --max_seq_length 512 \
                       --logging_steps 1000 \
                       --save_steps 4000 \
                       --do_eval \
```

- evaluate
```console
$ python3 evaluate_v1_0.py {$data_dir}/KorQuAD_v1.0_dev.json {$output_dir}/predictions_.json
```

## Results

- i-maunal test data로 학습, KorQuad Dev set으로 테스트한 결과


|                         | Exact Match (%) | F1 Score (%) |
| ----------------------- | --------------- | ------------ |
| mBERT                   |                 |              |

## References

- [KoBERT-KorQuAD](https://github.com/monologg/KoBERT-KorQuAD)

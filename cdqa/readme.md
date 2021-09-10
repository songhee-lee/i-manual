## 진행사항
- TF-IDF로 context top_n을 추출 -> QA 진행
- 질문에 tag 달아 contcat 후 결과 확인
- 내담자의 context 중에서만 question-paragraphs 유사도 분석 실시
  한 사람당 context : 13 ~ 15개
<br> 

## 1. Load Data
- I-manual data에서 제목(title), paragraph 정보만 가져온다.
- 내담자의 정보에 해당되는 정보만 뽑아낸다.
- 내담자의 정보(tag)를 paragraphs에 덧붙인다.

```
# 내담자 정보
paragraphs_tag = ['종족 - 스피드에너자이저', '사회적 성향 - 연구자/은근도전가(1/3)', 
				'에너지 흐름 - 한묶음흐름', '결정 방식 - 활력결정방식', '전략 - 에너자이저의 전략',
				'연료센터(DEFINED)', '활력센터(DEFINED)', '직관센터(DEFINED)', '감정센터(UNDEFINED)',
        '에고센터(DEFINED)', '방향센터(DEFINED)', '생각센터(UNDEFINED)', '영감센터(UNDEFINED)', '표현센터(DEFINED)']
```
<br>

## 2. Tokenizer
- 각 paragraphs 토큰화
- 불용어 및 특수기호 제거
- I-manual data 내 특수 단어 학습 (tokenizer update)

<br>

## 3. TF-IDF
- 내담자 질문에 tag 달기 : 진행 단계에 대한 정보가 될 것.
```
questions_tag = [ '종족', '사회적 성향', '에너지 흐름', '결정 방식', '전략', 
				'연료센터', '활력센터', '직관센터', '감정센터', '에고센터',
				'방향센터', '생각센터', '영감센터', '표현센터']
 ```
- TfidfVectorizer 이용해 tf-idf matrix 계산
  내담자의 전체 paragraph + 내담자의 question
- 해당 질문과 유사도가 가장 높은 top_n개 추출
<br>

## 4. Result
|categories|성공|애매|실패|
|------|---|---|---|
|20|5||
|1|2|1|
|3|||
|1|1|3|
|6|||
|5|||
- 성공 : 옳바른 paragraphs을 유사도 1위로 추출 성공
- 애매 
  a. 유사도 top3 안에 들지만 옳바른 paragraphs의 유사도가 1위가 아닌 경우
  b. 같은 title 안의 paragraphs이 나뉜 경우에서, 다른 paragraphs가 유사도 1위를 한 경우
- 실패 : 유사도 top 3 안에 옳바른 paragraphs이 없음

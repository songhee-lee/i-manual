def my_tokenizer(text):
    inputs = tokenizer(text, add_special_tokens=False, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    return text_tokens
  
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

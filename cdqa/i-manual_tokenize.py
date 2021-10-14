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

def remove_white_space_text(tokenized_paragraphs):
    tokenized_paragraphs_edit = []
    from text in tokenized_paragraphs:
        tokenized_paragraphs_eidt.append(remove_white_space(text))
    
    return tokenized_paragraphs_edit
        

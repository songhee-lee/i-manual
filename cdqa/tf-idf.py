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

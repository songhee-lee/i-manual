from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import pandas as pd
import random

model_path = "songhee/i-manual-mbert"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForQuestionAnswering.from_pretrained(model_path, return_dict=False)
def extract_metadata_from_data(num):
    metadata = {}
    if num==1:
        metadata = {"pn": "001", "ct": [1, 0, 1, 0, 0, 1, 1, 0, 0], "se": [1, 2, 0, 6], "t": 3, "p": 14, "d": 2}
    elif num==2:
        metadata = {"pn": "002", "ct": [0, 0, 1, 0, 0, 1, 1, 1, 1], "se": [0, 6, 2, 1], "t": 3, "p": 13, "d": 2}
    elif num==3:
        metadata = {"pn": "003", "ct": [1, 0, 1, 1, 1, 0, 1, 0, 0], "se": [6, 1, 3, 7], "t": 2, "p": 41, "d": 1}
    elif num==4:
        metadata = {"pn": "004", "ct": [0, 0, 0, 1, 0, 0, 1, 0, 0], "se": [3, 3, 7, 6], "t": 2, "p": 24, "d": 1}
    elif num==5:
        metadata = {"pn": "005", "ct": [0, 0, 0, 0, 0, 0, 0, 0, 0], "se": [1, 3, 6, 1], "t": 4, "p": 51, "d": 0}
    elif num==6:
        metadata = {"pn": "006", "ct": [0, 0, 0, 0, 0, 0, 0, 0, 0], "se": [5, 5, 5, 5], "t": 4, "p": 24, "d": 0}
    elif num==7:
        metadata = {"pn": "007", "ct": [0, 1, 1, 1, 0, 1, 1, 0, 0], "se": [1, 6, 1, 3], "t": 0, "p": 52, "d": 2}
    elif num==8:
        metadata = {"pn": "008", "ct": [1, 1, 0, 1, 1, 0, 0, 0, 0], "se": [4, 3, 6, 1], "t": 0, "p": 62, "d": 2}
    elif num==9:
        metadata = {"pn": "009", "ct": [1, 1, 1, 1, 1, 1, 1, 1, 1], "se": [3, 1, 1, 6], "t": 1, "p": 36, "d": 3}
    elif num==10:
        metadata = {"pn": "001", "ct": [1, 1, 1, 0, 0, 1, 1, 1, 0], "se": [2, 1, 6, 0], "t": 1, "p": 35, "d": 1}
    else:
        metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "se": [2, 0, 6], "t": 3, "p": 52, "d": 3}
    return metadata
def extract_metadata_from_tracker(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']

def koelectra_qa_getanswer(context, question):

    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    answer_start_scores, answer_end_scores = model(**inputs)
    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(
        answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer

def unego_get_question(ct, defined=False):
    question = ""
    # 0: 연료, 1: 활력, 2: 직관, 3: 감정, 4: 에고, 5: 방향, 6: 표현, 7: 생각, 8: 영감
    # 연료센터
    if ct == 0 and not defined:
        qlist_0 = [
            #"본인은 사람들에게 주목받으려고 애쓰는 편인가요?",
            #"본인은 말을 하지 하지 않아도 될 상황에서 대화를 트려고 애쓰는 편인가요?",
            #"본인은 늘 먼저 나서서 말을 하려고 하며 의사결정을 내려야 한다고 생각하시나요?"\
            "스트레스를 주변 사람에게 풀지는 않으실 것 같은데, 그렇죠?"
        ]
        question = random.choice(qlist_0)
        ego_comment = "일을 처리할 때 우선순위의 가치를 구분하는 능력이 있어요. 일을 빠르게 처리해야 한다는 압박에 불안해하며 조급해하지 않는 것이 좋아요."
        unego_comment = "무언가를 빨리 끝내기 위해 서두르다 보면 놓치는 부분도 많고 자칫 산만해 보일 수 있어요. 조급함을 잠시 내려놓고 서두를 가치가 있는지 없는지 구별하는 연습이 필요해요."

    elif ct == 0 and defined:
        qlist_0 = [
            "서두르다 일을 그르치거나 결과물에 만족하지 못하는 일은 없으실 것 같은데, 맞나요?"
        ]
        question = random.choice(qlist_0)
        ego_comment = "자신만의 일관성 있는 템포로 일을 처리하는 타입이네요! 일을 빠르게 처리해야 한다는 압박이 큰 스트레스로 오지 않도록 신경 써주세요."
        unego_comment = "무언가를 끝내야 한다는 압박이 큰 스트레스로 온다면 주변 사람들까지 힘들어질 수 있어요. 일을 처리할 때 들쑥날쑥한 속도가 아닌 원래 가지고 있는 나만의 템포를 찾아가는 연습이 필요해요. 그에 맞춰 주변 사람도 안정감 있게 일 처리를 할 테니까요."
    # 활력센터
    elif ct == 1 and not defined:
        qlist_1 = [
            "피곤함에 지쳐 있을 때면 그날 할 일은 뒤로 미룰 때가 있나요?"
        ]
        question = random.choice(qlist_1)
        ego_comment = "'당신은 '쉼'을 즐길 줄 알고 자신의 에너지를 적절히 사용하는 방법을 터득한 사람이에요. 하지만 갑자기 솟구치는 에너지만 믿고 무리해서 일하지 않도록 신경 써주세요."
        unego_comment = "갑자기 솟구치는 힘이 온전히 당신의 에너지가 아님을 의식해야 해요. 몸이 피로하다고 보내는 신호를 계속 무시하고 일에 박차를 가한다면 건강도 위협할 수 있답니다. '쉼'을 즐기고 받아들이는 연습이 필요해요."
    elif ct == 1 and defined:
        qlist_1 = [
            "아무리 바빠도 내가 사랑하는 일이라면 즐겁고 행복하시죠?"
        ]
        question = random.choice(qlist_1)
        ego_comment = "스스로가 진정 원하는 것을 알고, 적당한 바쁨을 즐길 줄 아는군요! 앞으로도 무언가 결정할 때 내 몸에서 나온 긍정적인 반응이 아닌 주변의 분위기에 휩쓸려 결정하지 않도록 주의해주세요."
        unego_comment = "주변 분위기에 휩쓸려 성급하게 결정해서 시작한 일이 있다면 피로감과 함께 스트레스까지 덤으로 얻을 거예요. 내가 선택한 일에 후회 없이 즐거워지려면 선택의 기로에 섰을 때 내 몸에서 반응하고 진정 원하는 것인 지 체크할 수 있는 인내심이 필요해요"
    # 직관센터
    elif ct == 2 and not defined:
        qlist_2 = [
            "나에게 좋지 못한 관계나 일에 엮이면 단호하게 끊어내는 편이신가요?",
        ]
        question = random.choice(qlist_2)
        ego_comment = "당신은 필요할 때 두려움과 맞설 용기가 충만한 사람이에요! 나에게 건강하지 않은 관계나 일 등이 엮였을 때 휘둘리지 않고 단호하게 직면하는 것이 좋아요."
        unego_comment = "나의 결단으로 인해 두려운 결과를 초래할까 봐 겁먹을 필요 없어요. 나와 엮인 관계나 일 등에서 옳지 않음을 느꼈다면 단호하게 놓아주고 필요할 때에는 두려움과 직면하는 연습이 필요해요."

    elif ct == 2 and defined:
        qlist_2 = [
            "결과를 깊게 생각하기 보다 즉각적인 '촉'을 따르는 경우가 많으신가요?"
        ]
        question = random.choice(qlist_2)
        ego_comment = "나에게 좋고 나쁜 영향을 주는 것을 구별하는 '촉'이 발달한 당신! 자신의 '촉'을 무시하고 '생각'의 흐름대로 결정하거나 행동하지 않도록 해야해요."
        unego_comment = "당신의 '순간의 본능'을 믿는 연습이 필요해요. 뭔가 쌔-한 느낌을 받았지만 그것을 무시하고 '생각'을 거쳐서 행동한다면 계속 근심과 의심에 휩싸여 두려움이 증폭될 거예요."

    # 감정센터
    elif ct == 3 and not defined:
        qlist_3 = [
            #"본인은 두려워서 차라리 말을 안하고 있나요?",
            #"본인은 말을 해서 화가 나게 될 것 같으면 차라리 말을 말자라며 혼자 끙끙하나요?"
            "다른 사람의 감정 변화를 잘 캐치하고 눈치껏 침묵하며 기다려주는 편이시죠?"
        ]
        question = random.choice(qlist_3)
        ego_comment = "주변의 감정 변화를 빠르게 캐치하며 공감해 주는 능력이 있는 당신! 진실을 알아내기 위해 다른 사람과 부딪히는 것을 두려워하거나 쉽게 동요되지 않도록 신경 써주세요."
        unego_comment = "혼자 있을 때에는 평온하지만 누구를 만났을 때 그 사람의 감정에 쉽게 동요되거나, 말 한마디에도 순간 욱- 한다거나, 혹은 감정적으로 부딪히는 것이 두려워지는 등 감정이 들쑥날쑥 해진다면 나의 감정이 아니라는 것을 의식하고 휘둘리지 않는 연습이 필요해요."

    elif ct == 3 and defined:
        qlist_3 = [
            "기분에 따라 충동적으로 의사결정을 하기보다 충분한 시간을 갖고 생각하는 편이신가요?"
        ]
        question = random.choice(qlist_3)
        ego_comment = "자신의 감정 변화를 객관적으로 보고 행동할 줄 아는 능력이 있어요. 앞으로도 감정에 휩쓸려 충동적인 결정을 하거나 그로 인해 주변에 영향을 주지 않도록 노력해주세요."
        unego_comment = "항상 누구를 만나서 무언가를 결정할 때 현재 감정 상태로 진행해도 괜찮을지 혹은 무리일지 시간을 두고 기다려 주는 것이 좋아요. 충동적인 결정에는 후회가 따라오고 그로 인한 감정의 영향으로 누군가를 힘들게 할 수 있기 때문이에요."

    # 에고센터
    elif ct == 4 and not defined:
        qlist_4 = [
            #"언제나 뭔가를 입증해야한다고 느끼고 생각하시나요?",
            #"나를 입증하기 위해 필요하지 않은 약속까지 하고 스스로를 괴롭히고 있지는 않은가요?"
            "지키지 못할 약속은 하지 않는 편이시죠?"
        ]
        question = random.choice(qlist_4)
        ego_comment = "자신의 가치를 있는 그대로 존중하며 남들에게 정당한 요구를 할 줄 아는 능력이 있어요. 하지만 나의 가치를 낮게 평가하는 순간 손해 보는 일이 생길 수 있어요."
        unego_comment = "항상 무언가 손해 보는 느낌이 들었다면 내가 정당한 요구를 해 본 적 있나 뒤돌아볼 필요가 있어요. 자신의 가치를 낮게 평가할수록 다른 사람에게 요구하기 힘들어지고 또 멋있게 보이기 위해 과잉 행동을 하기 때문이죠. 내 가치를 있는 그대로 존중하고 인정해 주는 연습이 필요해요."

    elif ct == 4 and defined:
        qlist_4 = [
            "사람들이 나의 가치를 몰라봐도 괜찮으신가요?"
        ]
        question = random.choice(qlist_4)
        ego_comment = "자신의 가치를 제대로 증명할 줄 알고 '계약'과 '흥정'에 탁월한 능력이 있어요. 이미 증명된 당신의 높은 가치를 일부러 티 내고 과시하지 않으면 더욱 좋은 결과가 있을 거에요."
        unego_comment = "겉으로 티 내고 과시 하지 않을수록 당신의 가치는 더욱 빛이 나요. 늘 신뢰와 겸손을 의식한다면 '계약'과 '흥정'에 능한 당신의 재능을 발휘할 수 있을 거예요."

    # 방향센터
    elif ct == 5 and not defined:
        qlist_5 = [
            #"본인은 끊임없이 사랑을 찾고 있는가요?",
            #"본인은 지속적으로 삶의 의미와 방향성을 찾고 있는가?",
            #"수시로 바뀌는 자신에게 늘 불안감을 느끼는가요?"
            "운명의 짝이라면 엄청난 노력을 쏟아붓지 않아도 나타날 것이라 생각하시나요?"
        ]
        question = random.choice(qlist_5)
        ego_comment = "어떤 장소와 사람이 나를 좋은 방향으로 이끌어 주는지 구별할 수 있어요. 그러니 인생의 방향과 목표를 찾으려 과하게 애쓰지 않는 것이 좋아요."
        unego_comment = "'나는 누구지?', '어떻게 살아가야 하지?', '뭘 해야 하지?' 등의 고민은 멈춰주세요. 구체적인 목표 점 보다는 좋은 장소와 좋은 사람을 거치면서 얻게 된 다양한 경험이 당신을 옳은 길로 인도할 거예요."

    elif ct == 5 and defined:
        qlist_5 = [
            "내가 하고 싶은 것, 원하는 것이 뚜렷한 편이신가요?"
        ]
        question = random.choice(qlist_5)
        ego_comment = "당신은 가고자 하는 길이 확실하고 스스로에게 비전이 있는 방향을 구별할 수 있어요. 다만, 여러 가지 근심과 걱정이 목표에 영향을 끼치지 않도록 신경 써주세요."
        unego_comment = "근심과 걱정이 당신의 방향성에 영향을 주고 있어요! 내가 가고자 하는 길이 확실하고 비전이 있다고 생각 된다면 믿어주세요. 그리고 주변에 알려주세요. '나만의 방향으로 잘 가고 있다'라고요."

    # 표현센터
    elif ct == 6 and not defined:
        qlist_6 = [
            #"본인은 끊임없이 사랑을 찾고 있는가요?",
            #"본인은 지속적으로 삶의 의미와 방향성을 찾고 있는가?",
            #"수시로 바뀌는 자신에게 늘 불안감을 느끼는가요?"
            "사람들 앞에 나서서 주목받는 건 별로 안좋아하시죠?"
        ]
        question = random.choice(qlist_6)
        ego_comment = "말할 기회가 주어졌을 때 숨겨왔던 말솜씨를 100% 발휘할 수 있는 능력이 있어요. 하지만 말을 함으로써 주목을 받고 싶어 하거나 근거 없는 말을 하는 것은 오히려 독이 될 수 있어요."
        unego_comment = "말하고 싶은 욕구를 못 참고 말을 꺼내기보다는 누군가 당신에게 의견을 묻거나 발언의 기회가 주어졌을 때 훨씬 자연스럽고 부담 없는 스피치를 할 수 있을 거예요."

    elif ct == 6 and defined:
        qlist_6 = [
            "말을 할 때 손동작이나 몸동작이 별로 없는 편이신가요?"
        ]
        question = random.choice(qlist_6)
        ego_comment = "어떤 상황에서 무슨 말을 해야 할지 정확한 구별할 수 있어요. 말할 때 과하게 에너지를 쓰거나 섣부르게 말을 하지 않도록 노력해야 해요."
        unego_comment = "지금이 내가 말을 꺼내도 되는 타이밍인지, 이 말을 해도 되는 상황인지 잘 구별할 줄 알고 기다릴 줄 안다면 사람들도 경계심 없이 경청하고 말하는 당신도 편안함을 느낄 거예요."

    # 생각센터
    elif ct == 7 and not defined:
        qlist_7 = [
            "사람들이 나를 똑똑한 사람으로 봐주지 않아도 괜찮으신가요?"
        ]
        question = random.choice(qlist_7)
        ego_comment = "흡수하는 정보마다 독특하고 유연하게 생각하는 능력이 있어요. 다만, 자유분방하게 생각하는 방식을 일관성 없다고 치부하지 않는 것이 좋아요."
        unego_comment = "논리적이고 똑똑해 보이려 노력할 필요 없어요. 당신은 흡수하는 정보마다 독특하고 유연하게 생각할 수 있는 능력이 있기 때문에 자신의 자유분방한 생각과 아이디어를 믿는 연습이 필요해요."

    elif ct == 7 and defined:
        qlist_7 = [
            "취향이 확고한 편이신가요?"
        ]
        question = random.choice(qlist_7)
        ego_comment = "당신은 답을 찾아내는 과정을 즐기는 사람이자 자신만의 생각과 의견이 뚜렷한 사람이에요. 나의 생각과 의견이 다른 사람에게 휘둘리지 않도록 노력해주세요."
        unego_comment = "나의 생각과 취향이 자주 바뀜을 느꼈다면 다른 사람으로 인해 영향을 받았을 확률이 높아요. 늘 생각과 의견을 어필할 때 나의 확고한 생각인지 다른 사람에게 휘둘린 건지 확인해 볼 필요가 있어요."

    # 영감센터
    elif ct == 8 and not defined:
        qlist_8 = [
            "흥미로운 정보를 발견하면 시간 가는 줄 모르고 빠져드는 편인가요?"
        ]
        question = random.choice(qlist_8)
        ego_comment = "무엇이 나에게 영감을 주는지, 혼란을 주는지 구별할 수 있어요. '다른 사람' 혹은 '나와 상관없는 문제'가 나의 머릿속을 지배하지 않도록 신경써야 해요."
        unego_comment = "'다른 사람' 혹은 '나와 상관없는 문제'가 나의 머릿속을 지배하도록 두지 마세요. 나에게 영감을 주고 도움이 되는 문제인지, 혼란을 주는 문제인지 구별할 연습이 필요해요."

    elif ct == 8 and defined:
        qlist_8 = [
            "새로운 정보를 받아들이는 과정에서 스트레스를 받지 않고, 편하게 받아들이나요?"
        ]
        question = random.choice(qlist_8)
        ego_comment = "당신은 무언가를 알아내려 애쓰지 않아도 자연스럽게 정보를 흡수하는 능력을 가졌어요. 다만, 어떠한 문제에 사로잡혀서 오랜 시간 고민하거나 조급해지지 않도록 신경 써주세요."
        unego_comment = "무엇을 알아내려고 집요하게 파고들려 하면 근심과 스트레스로 힘들 수 있어요. 인내심을 가지고 정보가 흡수되는 과정을 즐기면 자연스럽게 알게 될 테니 조급해 하지 마세요."

    question_intro = [
        "제가 질문 한가지 할게요! 질문을 보시고 솔직하게 답변해주시면 됩니다 :)",
        "지금까지 설명을 토대로 내담자님의 성향에 대해서 한가지 질문할게요!!",
        "잘 따라오고 계신가요? 내담자님의 성향을 파악하기 위해서 질문 하나 드릴게요 :)"
    ]
    q_intro = random.choice(question_intro)
    return [q_intro, question, ego_comment, unego_comment]

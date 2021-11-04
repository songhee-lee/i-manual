from transformers import BertTokenizer, BertForQuestionAnswering, AutoConfig
import torch
import pandas as pd
import random


model_path = "songhee/i-manual-mbert"
config = AutoConfig.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForQuestionAnswering.from_pretrained(model_path, config=config)
def extract_metadata_from_data(tracker): #추후 삭제이후 각 파일의 import부분도 삭제
    #if num==1:
    #    metadata = {"pn": "001", "ct": [1, 0, 1, 0, 0, 1, 1, 0, 0], "se": [1, 2, 0, 6], "t": 3, "p": 14, "d": 2}
    #elif num==2:
    #    metadata = {"pn": "002", "ct": [0, 0, 1, 0, 0, 1, 1, 1, 1], "se": [0, 6, 2, 1], "t": 3, "p": 13, "d": 2}
    #elif num==3:
    #    metadata = {"pn": "003", "ct": [1, 0, 1, 1, 1, 0, 1, 0, 0], "se": [6, 1, 3, 7], "t": 2, "p": 41, "d": 1}
    #elif num==4:
    #    metadata = {"pn": "004", "ct": [0, 0, 0, 1, 0, 0, 1, 0, 0], "se": [3, 3, 7, 6], "t": 2, "p": 24, "d": 1}
    #elif num==5:
    #    metadata = {"pn": "005", "ct": [0, 0, 0, 0, 0, 0, 0, 0, 0], "se": [1, 3, 6, 1], "t": 4, "p": 51, "d": 0}
    #elif num==6:
    #    metadata = {"pn": "006", "ct": [0, 0, 0, 0, 0, 0, 0, 0, 0], "se": [5, 5, 5, 5], "t": 4, "p": 24, "d": 0}
    #elif num==7:
    #    metadata = {"pn": "007", "ct": [0, 1, 1, 1, 0, 1, 1, 0, 0], "se": [1, 6, 1, 3], "t": 0, "p": 52, "d": 2}
    #elif num==8:
    #    metadata = {"pn": "008", "ct": [1, 1, 0, 1, 1, 0, 0, 0, 0], "se": [4, 3, 6, 1], "t": 0, "p": 62, "d": 2}
    #elif num==9:
    #    metadata = {"pn": "009", "ct": [1, 1, 1, 1, 1, 1, 1, 1, 1], "se": [3, 1, 1, 6], "t": 1, "p": 36, "d": 3}
    #elif num==10:
    #    metadata = {"pn": "001", "ct": [1, 1, 1, 0, 0, 1, 1, 1, 0], "se": [2, 1, 6, 0], "t": 1, "p": 35, "d": 1}
    #else:
    #    metadata = {"pn": "김재헌", "ct": [1, 0, 0, 1, 1, 1, 1, 0, 0], "se": [1, 2, 0, 6], "t": 3, "p": 52, "d": 3}
    pn = tracker.get_slot("pn")
    t = tracker.get_slot("t")
    p = tracker.get_slot("p")
    d = tracker.get_slot("d")
    ct = tracker.get_slot("ct")
    se = tracker.get_slot("se")
    metadata = {"pn": f"{pn}", "t": t, "p": p, "d": d, "ct": ct, "se": se}
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
    answer_start_scores, answer_end_scores = model(**inputs, return_dict=False)
    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(
        answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer

def unego_get_question(ct, unego_count, defined=False):
    question = ""
    # 0: 연료, 1: 활력, 2: 직관, 3: 감정, 4: 에고, 5: 방향, 6: 표현, 7: 생각, 8: 영감
    # 연료센터
    if ct == 0 and not defined:
        qlist_0 = [
            "마감일을 못 지킬까봐 불안하고 스트레스를 받는 편인가요?",
            "서두르다 일을 그르치거나 결과물에 만족하지 못한 적이 많은 편인가요?",
            "인생에서 무언가를 이뤄야만 한다는 생각이 늘 자리 잡고 있나요?"
        ]
        question = qlist_0[unego_count]
        ego_comment = "당신에게 그 어떤 압박이나 스트레스가 온다고 무조건 휘둘릴 필요는 없어요.당신이 진정 원하는 일에만 서두름을 갖으세요"
        unego_comment = "무언가를 빨리 끝내기 위해 서두르다 보면 놓치는 부분도 많고 자칫 산만해 보일 수 있어요. 조급함을 잠시 내려놓고 서두를 가치가 있는지 없는지 구별하는 연습이 필요해요."

    elif ct == 0 and defined:
        qlist_0 = [
            "스트레스를 주변 사람에게 푸는 편인가요?",
            "다른 사람의 굼뜬 행동을 보면 답답해서 한마디씩 하는 편인가요?",
            "나와 다른 방식으로 일처리 하는 사람이 종종 이해하기 힘든가요?"
        ]
        question = qlist_0[unego_count]
        ego_comment = "당신 자신의 흐름을 믿고 그 어떤 압박이나 재촉에도 당신만의 흐름을 잘 조절 할 수 있는 능력을 활용해보세요"
        unego_comment = "무언가를 끝내야 한다는 압박이 큰 스트레스로 온다면 주변 사람들까지 힘들어질 수 있어요. 일을 처리할 때 들쑥날쑥한 속도가 아닌 원래 가지고 있는 나만의 템포를 찾아가는 연습이 필요해요. 그에 맞춰 주변 사람도 안정감 있게 일 처리를 할 테니까요."
    # 활력센터
    elif ct == 1 and not defined:
        qlist_1 = [
            "밖에서는 괜찮은데 집에만 오면 체력이 급 방전되는 편인가요?",
            "피곤함에 지쳐 있을 때도 그날 할 일은 끝마치려 하나요?",
            "쉬고 있으면 오히려 불안하고, 할 일을 찾아서 하는 편인가요?"
        ]
        question = qlist_1[unego_count]
        ego_comment = "당신은 매우 자유롭게 당신의 활력 센터를 쓸 수 있답니다 당신이 원하면 당신은 자유로울 수 있어요"
        unego_comment = "갑자기 솟구치는 힘이 온전히 당신의 에너지가 아님을 의식해야 해요. 몸이 피로하다고 보내는 신호를 계속 무시하고 일에 박차를 가한다면 건강도 위협할 수 있답니다. '쉼'을 즐기고 받아들이는 연습이 필요해요."
    elif ct == 1 and defined:
        qlist_1 = [
            "주변 분위기에 휩쓸려 원치않는 결정을 하고 후회하는 편인가요?",
            "하루를 마칠 때 만족감보다 피로감이 앞서나요?",
            "아무리 바빠도 내가 사랑하는 일이라면 즐겁고 행복한가요?"
        ]
        question = qlist_1[unego_count]
        ego_comment = "당신은 그야말로 열정의 대가입니다. 당신이 진정 원하는것을 하고자 한다는 결의가 있다면 반드시 이뤄질거예요"
        unego_comment = "주변 분위기에 휩쓸려 성급하게 결정해서 시작한 일이 있다면 피로감과 함께 스트레스까지 덤으로 얻을 거예요. 내가 선택한 일에 후회 없이 즐거워지려면 선택의 기로에 섰을 때 내 몸에서 반응하고 진정 원하는 것인 지 체크할 수 있는 인내심이 필요해요"
    # 직관센터
    elif ct == 2 and not defined:
        qlist_2 = [
            "나에게 좋지 못한 관계나 일에 엮이면 단호하게 끊어내는 편인가요?",
            "아직 일어나지 않은 일들을 미리 걱정하는 편인가요?",
            "챙겨 먹는 영양제를 하루라도 거르면 불안한 편인가요?"
        ]
        question = qlist_2[unego_count]
        ego_comment = "당신이 갑자기 기분이 나빠진다면 그 느낌을 신뢰하고 그곳을 떠나도 좋아요"
        unego_comment = "나의 결단으로 인해 두려운 결과를 초래할까 봐 겁먹을 필요 없어요. 나와 엮인 관계나 일 등에서 옳지 않음을 느꼈다면 단호하게 놓아주고 필요할 때에는 두려움과 직면하는 연습이 필요해요."

    elif ct == 2 and defined:
        qlist_2 = [
            "나에게 나쁜 영향을 주는 사람을 구분하기 어렵나요?",
            "결과를 깊게 생각하기 보다 즉각적인 '촉'을 따르는 경우가 많나요?",
            "미래, 건강, 실패에 대해 늘 두렵고 안정감을 못 느끼는 편인가요?"
        ]
        question = qlist_2[unego_count]
        ego_comment = "당신은 마치 즉흥연주자 처럼 당신의 기분좋은 느낌을 바로바로 다른 사람들에게도 나눠줄 수 있는 멋진 사람입니다."
        unego_comment = "당신의 '순간의 본능'을 믿는 연습이 필요해요. 뭔가 쌔-한 느낌을 받았지만 그것을 무시하고 '생각'을 거쳐서 행동한다면 계속 근심과 의심에 휩싸여 두려움이 증폭될 거예요."

    # 감정센터
    elif ct == 3 and not defined:
        qlist_3 = [
            "'착한 아이 콤플렉스'가 있는 것 같나요? ",
            "불만이 있어도 싸움이 될까봐 꾹 참는 편인가요?",
            "다른 사람의 감정 변화를 잘 캐치하고 눈치껏 침묵하며 기다려주는 편인가요?"
        ]
        question = qlist_3[unego_count]
        ego_comment = "타인의 감정에도 잘 공감해주는 당신은 정말 스윗하고 따뜻한 사람이예요."
        unego_comment = "혼자 있을 때에는 평온하지만 누구를 만났을 때 그 사람의 감정에 쉽게 동요되거나, 말 한마디에도 순간 욱- 한다거나, 혹은 감정적으로 부딪히는 것이 두려워지는 등 감정이 들쑥날쑥 해진다면 나의 감정이 아니라는 것을 의식하고 휘둘리지 않는 연습이 필요해요."

    elif ct == 3 and defined:
        qlist_3 = [
            "기분에 따라 충동적으로 의사결정을 하기보다 충분한 시간을 갖고 생각하는 편인가요?",
            "'기분이 태도가 되지 말자'라는 문구를 보면 조금 찔리나요?",
            "나의 감정 상태가 주위에 영향을 끼치는 것을 알지만 숨기기 힘든 편인가요?"
        ]
        question = qlist_3[unego_count]
        ego_comment = "때때로 답답함이 느껴질지라도그 과정을 인내하고 기다리세요 분명 당신은 뛸듯이 기쁜 결과물을 얻게 될거예요"
        unego_comment = "항상 누구를 만나서 무언가를 결정할 때 현재 감정 상태로 진행해도 괜찮을지 혹은 무리일지 시간을 두고 기다려 주는 것이 좋아요. 충동적인 결정에는 후회가 따라오고 그로 인한 감정의 영향으로 누군가를 힘들게 할 수 있기 때문이에요."
    # 에고센터
    elif ct == 4 and not defined:
        qlist_4 = [
            "지갑 사정에 비해 충동적으로 큰돈을 쓰고 후회하는 편인가요?",
            "지키지 못할 약속은 하지 않는 편인가요?",
            "자존감이 높은 것 처럼 행동하지만 사실은 연기일 뿐인가요?"
        ]
        question = qlist_4[unego_count]
        ego_comment = "당신은 굳이 세상에 자신을 입증하려고 애쓰지 않아도 된답니다."
        unego_comment = "항상 무언가 손해 보는 느낌이 들었다면 내가 정당한 요구를 해 본 적 있나 뒤돌아볼 필요가 있어요. 자신의 가치를 낮게 평가할수록 다른 사람에게 요구하기 힘들어지고 또 멋있게 보이기 위해 과잉 행동을 하기 때문이죠. 내 가치를 있는 그대로 존중하고 인정해 주는 연습이 필요해요."

    elif ct == 4 and defined:
        qlist_4 = [
            "사람들이 나의 가치를 몰라보면 자존심이 상하나요?",
            "타인의 답답한 모습을 보면 '왜 나같이 못하지..?'라는 생각을 하나요?",
            "내 평판과 이미지가 안 좋아지면 억울하고 화가 나는 편인가요?"
        ]
        question = qlist_4[unego_count]
        ego_comment = "당신의 변함없는 의지력이 멋지게 발현된다면 다른 많은 사람들에게 꿈과 용기를 북돋워준답니다."
        unego_comment = "겉으로 티 내고 과시 하지 않을수록 당신의 가치는 더욱 빛이 나요. 늘 신뢰와 겸손을 의식한다면 '계약'과 '흥정'에 능한 당신의 재능을 발휘할 수 있을 거예요."

    # 방향센터
    elif ct == 5 and not defined:
        qlist_5 = [
            "나는 누구이며, 나만의 정체성이 무엇인지 계속 확인하려 하나요?",
            "운명의 짝이라면 엄청난 노력을 쏟아붓지 않아도 나타날 것이라 생각하는 편인가요?",
            "앞으로 어떻게 살아가야 할지 막막할 때가 많은 편인가요?"
        ]
        question = qlist_5[unego_count]
        ego_comment = "당신의 변화무쌍함은 오히려 당신을 새로운 멋진 미지의 탐험자로 만들어 준답니다."
        unego_comment = "'나는 누구지?', '어떻게 살아가야 하지?', '뭘 해야 하지?' 등의 고민은 멈춰주세요. 구체적인 목표 점 보다는 좋은 장소와 좋은 사람을 거치면서 얻게 된 다양한 경험이 당신을 옳은 길로 인도할 거예요."

    elif ct == 5 and defined:
        qlist_5 = [
            "내가 하고 싶은 것, 원하는 것이 뚜렷한 편인가요?",
            "사람들이 잘못된 방향으로 가는 것 같으면 나서서 말리는 편인가요?",
            "이상형이나 삶의 목표가 자주 바뀌는 편인가요?"
        ]
        question = qlist_5[unego_count]
        ego_comment = "당신의 명료하고 확고한 방향성은 다른 많은 사람들에게도 가이드라인이 되어주기도 한답니다."
        unego_comment = "근심과 걱정이 당신의 방향성에 영향을 주고 있어요! 내가 가고자 하는 길이 확실하고 비전이 있다고 생각 된다면 믿어주세요. 그리고 주변에 알려주세요. '나만의 방향으로 잘 가고 있다'라고요."

    # 표현센터
    elif ct == 6 and not defined:
        qlist_6 = [
            "사람들과 있을 때 침묵을 견디기 힘든 편인가요?",
            "사람들 앞에 나서서 주도적으로 얘기하고 주목받고 싶어하나요?",
            "가만히 있으면 바보처럼 보일까 봐 일단 아무 말이나 하고 보는 편인가요?"
        ]
        question = qlist_6[unego_count]
        ego_comment = "당신은 때론 침묵하고 있지만 마치 거짓말 탐지기 처럼 누가 옳은말을 하는지 알수도 있는 능력의 소유자예요"
        unego_comment = "말하고 싶은 욕구를 못 참고 말을 꺼내기보다는 누군가 당신에게 의견을 묻거나 발언의 기회가 주어졌을 때 훨씬 자연스럽고 부담 없는 스피치를 할 수 있을 거예요."

    elif ct == 6 and defined:
        qlist_6 = [
            "나서면 안 되는 타이밍에 말을 하고 후회한 적이 많나요?",
            "누군가와 대화를 하거나 발표를 하고 나면 에너지를 다 소진한 느낌이 드나요?",
            "말을 할 때 손동작이나 몸동작이 큰 편인가요?"
        ]
        question = qlist_6[unego_count]
        ego_comment = "당신이 잘 알고 준비된 맨트들을 하게 될때 사람들은 당신의 매력에 빠지게 될거예요"
        unego_comment = "지금 내가 말을 꺼내도 되는 타이밍인지, 이 말을 해도 되는 상황인지  잘 구별할 줄 알고 기다릴 줄 안다면 사람들도 경계심 없이 경청하고 말하는 당신도 편안함을 느낄 거예요."

    # 생각센터
    elif ct == 7 and not defined:
        qlist_7 = [
            "내 생각이 논리적이고 일관성 있다는 것을 어필하고 싶어하나요?",
            "내 생각이 정답이 아닌 것 같아 불안할 때가 많은가요?",
            "사람들이 나를 똑똑한 사람으로 봐주길 바라나요?"
        ]
        question = qlist_7[unego_count]
        ego_comment = "당신의 스폰치처럼 정보를 빨아들이는 능력은 정말 대단합니다."
        unego_comment = "논리적이고 똑똑해 보이려 노력할 필요 없어요. 당신은 흡수하는 정보마다 독특하고 유연하게 생각할 수 있는 능력이 있기 때문에 자신의 자유분방한 생각과 아이디어를 믿는 연습이 필요해요."

    elif ct == 7 and defined:
        qlist_7 = [
            "나는 취향이 확고한 편인가요?",
            "무언가를 이해하려 끝없이 생각하며 스트레스를 받는 편인가요?",
            "나는 주변에 의해 생각이 자주 바뀌는 편인가요?"
        ]
        question = qlist_7[unego_count]
        ego_comment = "당신은 떠오르는 생각들을 따지듯 분석하며 즐겨도 괜찮아요"
        unego_comment = "나의 생각과 취향이 자주 바뀜을 느꼈다면 다른 사람으로 인해 영향을 받았을 확률이 높아요. 늘 생각과 의견을 어필할 때 나의 확고한 생각인지 다른 사람에게 휘둘린 건지 확인해 볼 필요가 있어요."

    # 영감센터
    elif ct == 8 and not defined:
        qlist_8 = [
            "다른 사람의 문제를 해결하려 들거나 참견하는 편인가요?",
            "다단계, 종교 단체의 제안에 흔들린 적이 있나요?",
            "흥미로운 정보를 발견하면 시간 가는 줄 모르고 빠져드는 편인가요?"
        ]
        question = qlist_8[unego_count]
        ego_comment = "중요하지 않은 영감은 그냥 아~ 하고 떠나 보내도 좋아요."
        unego_comment = "'다른 사람' 혹은 '나와 상관없는 문제'가 나의 머릿속을 지배하도록 두지 마세요. 나에게 영감을 주고 도움이 되는 문제인지, 혼란을 주는 문제인지 구별할 연습이 필요해요."

    elif ct == 8 and defined:
        qlist_8 = [
            "사소한 문제도 오랜 시간 고민하는 편인가요?",
            "새로운 정보를 받아들이는 과정에서 스트레스를 받는 편인가요?",
            "문제를 빨리 해결하려 섣부른 의사결정을 자주 하는 편인가요?"
        ]
        question = qlist_8[unego_count]
        ego_comment = "당신의 영감은 당신 뿐만 아니라 다른 이들에게도 정신적으로 좋은 영감을 준답니다"
        unego_comment = "인내심을 가지고 정보가 흡수되는 과정을 즐기면 자연스럽게 알게 될 테니 조급해 하지 마세요."


    return [question, ego_comment, unego_comment]
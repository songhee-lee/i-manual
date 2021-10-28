import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused
from actions.common import extract_metadata_from_tracker

logger = logging.getLogger(__name__)
class ActionLeadingAuthority(Action):
    def name(self) -> Text:
        return "action_leading_authority"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_authority')

        metadata = extract_metadata_from_tracker(tracker)

        dispatcher.utter_message(
            f'다음으로 당신의 결정방식에 대해 살펴보겠습니다.')

        if metadata["a"] == 0:
            h_type = "감정 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_0.png"
            msg = "지금 당신의 기분은 어떤가요? 좋은가요? 나쁜가요? 기쁜가요? 슬픈가요? 당신이 느끼고 있는 감정이 무엇이든지 '지금 이 순간'에는 당신에게 무엇을 결정 할 만한 때가 아닙니다. 지금 이 순간에는 기분이 좋다가도 금방 나빠지기도 하고, 또 다음 순간에는 기쁘다가도 슬퍼질 수 있는 것이 바로 감정입니다."
            msg2 = "당신은 이렇게 시시각각 변화하는 다양한 감정을 가지고 있는 사람입니다. 이렇게 지속적으로 감정이 영향을 미치고 있는 지금 이 순간에 곧바로 결정을 내릴 경우, 그 결과는 몹시도 불만족스러울 수 있습니다. 자신의 감정이 어떤지는 스스로 잘 알고 있을 수도 모를 수도 있지만, 분명한 것은 당신의 감정은 늘 파도가 치는 것처럼 위 아래로 움직이고, 무드가 좋았다가 나빴다가 하는 움직임 속에 있다는 것입니다."
            msg3 = "한 순간 기분이 좋아서 흔쾌히 결정을 내렸을 때, 혹은 기분이 안좋아서 결정을 보류하고 미뤘다가 기회를 놓쳤을 때. 양 쪽 모두 결국에는 후회스러울 수 있습니다. 당신이 결정을 내리던 그때의 그 감정, 그 기분은 이미 파도처럼 지나간 순간이기 때문입니다. 예를 들어 쇼핑을 하고 나서 후회하는 일은 일상입니다. ’아무래도 이건 아닌것 같아. 바꿔야겠어. 환불 해야겠어…’ 하고 마음이 바뀌는건 너무나 흔한 일입니다. 밖에서 물건을 사던 때의 기분은 이미 지나가고, 집에 돌아왔을 때에는 감정이 새롭게 변했기 때문입니다. "
            msg4 = "사온 물건에 대한 감정이 달라진 것입니다. 물론 이런 기분은 한참이 흐르고 나서 느껴질 수도 있습니다. 당신의 감정이 좋을 때에는 무엇이든 ‘Yes’ 하고 허락하기 쉽습니다. 반면에 감정이 안좋을 때에는 ‘No’ 하고 모든게 다 싫고 거부합니다. 그렇기 때문에 순간의 자신의 감정에 따라 무언가를 결정하고 행동하는 것은 만족스럽지 않은 결과로 이어집니다. "
            msg5 = "언제나 감정의 에너지가 높게, 혹은 낮게, 파도를 넘나드는 당신에게, 무엇이 옳은지 진실은 절대 지금 이 순간에 있지 않습니다. 감정의 높고 낮은 파도를 한 번 지나고서 감정이 높지도 낮지도 않은 중간쯤 잠잠해지는 고요한 그 어느 때야 말로 당신이 결정을 할 때입니다. 좋은 감정이나 혹은 나쁜 감정 그 어디에도 치우쳐지지 않은 그때야 말로 무엇이 진실인지 알 수 있는 때인 것입니다. 파도에 올라타 있는 동안에는 내가 지금 높이 올라와 있는지, 혹은 낮게 내려와 있는지 알지 못합니다."
            msg6 = "한 번의 파도가 흘러 지나도록 시간을 들여 바라본다면, 지나간 시간에 나의 감정이 높았는지 낮았는지 알 수 있게 됩니다. 바로 그 고요한 순간에 결정을 하는 것이 당신에게 긍정적 결과를 가져올 것입니다.만약 ‘이렇게 해야지!’하고 마음 먹었는데 어떤 감정의 파도가 일렁이고 있는 중이라면, 아직은 결정할 때가 아닙니다. 자기자신을 조금 더 기다려 줄 필요가 있습니다."
            tag = "감정의 노예,시간이 필요해"
        elif metadata["a"] == 1:
            h_type = "활력 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_1.png"
            msg = "에너지(활력)가 있는지 없는지에 따라 결정하는 것이 당신에게 맞는 결정방식입니다. 에너지가 있는지 없는지라는 것은 생각이 아닌 몸으로 느낄 수 있는 느낌인데 “뭔가 움찔하듯” 몸에서 솟아나는 반응을 말하는 것 입니다."
            msg2 = "이 결정 방식을 지닌 당신은 에너자이저 종족 또는 스피드 에너자이저 종족입니다."
            msg3 = "이 반응은 “응! 어!” 또는 ”흠...” “아니.” 등의 소리와 비슷한 느낌이며, 동시에 몸이 약간이라도 스프링처럼 튀어오르는 듯한 활력에너지의 반응은 에너자이저 종족들에게 질문이 던져 졌을 때, 즉각적으로 몸에서 느껴지는 것입니다. 당신에게 결정할 것에 대한 질문이 던져 졌을 때, 주저함이 느껴진다면(애매모호할 때), “지금은 잘 모르겠네~ 나중에 다시 질문해줄래요?” 가 정답입니다."
            msg4 = "이 결정 방식은 에너자이저들에게 활력 에너지의 반응을 통해, 무엇이 자신에게 옳고, 어디까지가 자신의 참여 범위인지 등등 내면의 진실을 알 수 있게 해줍니다. 어떤 질문이 들어왔을때 그 질문에 답변하는 그 순간, '예스~' 혹은 '노'라고 느껴지는 결정에 대한 답이 있습니다. 질문을 받았을 때, 활력 에너지를 통한 당신의 몸의 반응은 그 결정이 당신에게 좋은지, 아닌지를 알려 줍니다."
            msg5 = "긍정의 반응이라면, 에너지가 있는, 힘이 넘치는듯 움찔하며 마치 엉덩이가 살짝 들썩이는듯한 느낌을 받을 것입니다. 하지만 부정의 반응이라면 에너지가 없는, 힘이 빠지는 듯~ 마치 몸이 뒤로 물러나는듯한 느낌을 받을 것입니다.이 결정방식을 머리로 이해했다고 하여 한 번에 곧장 몸의 반응으로 연결하여 알아차리기는 힘들 수도 있습니다."
            msg6 = "꾸준하게 자신에게 오는 질문들에서 느껴지는 자신의 몸의 반응을 살피는 연습을 통하여 활력센터의 감각을 되살릴 수 있습니다. 자신에게 주어진 진실이 무엇인지 즉시 알아볼 수 있는 이 놀라운 도구를 적극 사용하길 권합니다."
            tag = "즉각적인 촉,Yes or No"            
        elif metadata["a"] == 2:
            h_type = "직관 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_2.png"
            msg = "섬세하게 찾아오는 순간의 직관에 따라 결정을 했을 때 당신의 몸은 안전할 수 있습니다. 직관은 어떤 사람이나 무언가에 대해서 아주 즉각적인 공명이나 인식을 느끼는 것이며, 당신은 그 사람이나 무언가가 안전한지 아닌지를 구별하는 것입니다."
            msg2 = "당신은 미묘한 변화를 민감하게 느껴야 하며, 언제라도 그 직관(섬세한 느낌)을 믿고 삶을 움직일 수 있어야 합니다. 이러한 직관의 신호는 아주 작게 전달되며 단 한 번의 기회 뿐입니다. "
            msg3 = "외부로부터 오는 여러 압박이나 생각으로 인해 직관을 무시하고 고민하며 계산하거나 의심한다면, 당신은 위험에 처할 수 있습니다. 오랜 시간을 심사숙고하여 결정하는 것은 당신에게 맞지 않습니다. "
            msg4 = "결정은 반드시 지금, 이 순간에 내려지는 것입니다. 잠시라도 주저한다면 직관은 사라질 것입니다."
            msg5 = "직관은 미래에 대해 알지 못합니다. ‘10분만, 한 시간 뒤에, 하루만 있다가’ 하면서 그 순간을 지나친다면, 결정은 바뀔 수 있습니다. 어떤 것이 자신에게 안전하다면 본능적으로 지금, 이 순간에 바로 알게 될 것입니다. 반대로 자신에게 해롭거나 위험한 것도 똑같이 알 수 있습니다. "
            msg6 = "힘들겠지만 당신이 맞는 결정을 하기 위해서는 자신의 직관의 신호를 신뢰해야 합니다."
            tag = "생존 본능을 따라,주저하지 말 것"
        elif metadata["a"] == 3:
            h_type = "에고현시 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_3.png"
            msg = "혁신주도가의 에고현시 결정 방식은 “나 이거 할거야. 나 할 수 있어. 나 하는 사람이야. 내가 이것도 못할 것 같아?” 등등. 자신이 어떤 결정을 원하는지 알기 위해 자신이 하는 말을 스스로 잘 들어봐야 합니다."
            msg2 = "머리 속에 떠오르는 생각이 아닌, 입을 통해 밖으로 표현되는 자신이 말을 직접 들어보고 결정해야 합니다."
            msg3 = "당신은 자신이 한 말 속에 무엇을 어떻게 결정할지 진실이 담겨있습니다. 주변 사람들에게 말로 표현을 함으로서 자신의 의지를 표현함과 동시에 자신의 결정을 알리는 것입니다. 그것이 삶을 이끌고 새로운 것을 시작하게 할 것입니다."
            msg4 = "당신은 의지력을 발휘하여 약속을 만들고, 그것을 지킬 때 건강합니다. 하지만 의지력은 한계가 있으니 일과 휴식의 균형을 가지고 있어야 하겠죠. 에고센터와 관련이 있는 장기는 바로 심장인데, 심장에 큰 부담을 주지 않기 위해서는 어떤 장기적인 일을 시작할 때에는 반드시 그것이 자신에게 옳은 일인지 확인한 후에 결정해야 합니다."
            msg5 = "그릇된 결정은 심장에 과부하를 주면서까지 그 약속을 이행하기 위해 몸을 혹사시킬 것입니다."
            msg6 = "일을 한만큼 휴식하고 노는 시간을 가져야합니다. 이 균형을 유지하는 것은 에너지적으로도, 육체적으로도 필수입니다."
            tag = "내 안의 소리가 들려,나 중심의 선택"
        elif metadata["a"] == 4:
            h_type = "방향성 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_4.png"
            msg = "결정해야 할 무언가에 대해 자신이 무슨 말을 하는지 들어보는 과정을 거치는 것이 당신의 결정 방식입니다. 이 결정 방식을 지닌 당신은 가이드 종족인데요. "
            msg2 = "다른 사람이나 세상으로부터 초대를 받았을 때 생겨나는 반응 속에 당신이 알아야 하는 모든 것이 들어 있습니다. 자신에게 맞는 결정에 대한 진실은 항상 정체성을 통해 표현됩니다."
            msg3 = "결정할 것에 대한 표현에 자신을 위한 무언가가 담겨있지 않다면, 거기에는 당신을 위한 성공은 없습니다. 초대가 온 것에 대해 자신이 하는 말을 들어보세요."
            msg4 = "무엇이 나에게 기쁨을 주는지, 무엇이 나를 나 답게 느끼게 하는지에 따라 결정하는 사람입니다. "
            msg5 = "스스로에게 소리내어 질문을 던져보세요. ‘이 결정을 하면 나는 행복할까? 이것을 통해 나를 표현할 수 있을까? 이게 나에게 맞는 방향 일까?’ 결정을 하기 전, 주변 사람들과 대화를 나누며 자신이 결정할 것에 대해 어떻게 말하고 있는지 들어보는 것은 매우 도움이 됩니다. "
            msg6 = "되도록 여러 사람과 대화를 해보는 것이 좋습니다. 또한 자기 자신의 말을 들어보는 것을 통해 나를 위해 옳은 방향이 무엇인지 알 수 있습니다."
            tag = "나를 위한 선택,주변 사람들과 대화"
        elif metadata["a"] == 5:
            h_type = "에고투사 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_5.png"
            msg = "가이드 종족의 에고투사 결정방식은 “내가 원하는게 뭘까? 나를 위한 것이 뭐가 있을까? 내가 그것을 할 수 있을까?“ 하는 자신을 위한 질문을 스스로에게 던져봐야 합니다. 당신은 스스로 묻고 답하는 시간을 통해 '이건 좋은 것 같아' 하는 의지력을 느끼거나, 혹은 어떤 의지도 느끼지 못할 것입니다."
            msg2 = "특히 가이드 종족인 당신은, 다른 사람이나 세상으로부터 자신의 능력을 인정받고, 우리와 함께 하자고 초대를 기다려야 합니다. 어떤 초대가 왔을 때에는, 그 초대를 받아들일지 아닌지에 대해 스스로 질문을 던져보며 자신에게 의지력이 생기는지 안생기는지 살펴보고 결정해야 합니다. "
            msg3 = "의지력이 있고/없고가 당신의 결정에 주요하게 작용합니다. 당신은 의지력을 발휘하여 약속을 만들고, 그것을 지킬 때 건강합니다. 이러한 의지력에는 한계가 있기에, 늘 일과 휴식의 균형을 잊지 말아야 합니다."
            msg4 = "에고센터는 실제로 심장건강과 관련이 있는데, 에고센터가 정의된 사람들은 약속을 만들고, 그 약속을 지키고자 의지를 만들어서 쓰고, 정말로 그 약속을 지켜낼 때 건강합니다. "
            msg5 = "심장에 부담을 주지 않기 위해서는, 어떤 장기적인 일을 시작할 때에는 반드시 그것이 자신에게 옳은 일인지 확인한 후에 결정해야 합니다. "
            msg6 = "일한 만큼 휴식하고 노는 시간을 가져야합니다. 이 균형을 유지하는 것은 에너지적으로도, 육체적으로도 필수입니다."
            tag = "주변 환경의 영향,대화가 필요해"
        elif metadata["a"] == 6:
            h_type = "외부환경 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_6.png"
            msg = "나만의 내부 결정방식을 가지고 있지 않은 당신은 외부환경 결정방식을 가지게 됩니다.자신만의 고유한 결정방식을 가진 다른 사람들에 비해서 결정을 내릴 때 더 많은 시간을 필요로 합니다. 빨리 결정을 내리라고 누군가가 재촉할 경우 도무지 뭘 선택해야 할지 몰라서 조바심이 생기거나 불편함을 느꼈을 수 있습니다."
            msg2 = "자신을 둘러싼 다른 사람이나 다른 무언가 등등, 주변 환경의 느낌이 썩 좋지 않다면, 그것에서 만들어지는 협상, 주고받는 아이디어들 역시 좋을 리 없습니다. 당신이 스스로에게 가장 먼저 던져봐야 하는 질문은 ‘지금 이 환경이 나에게 적합한가? 내가 지금 좋은 환경에 있나?’ 입니다."
            msg3 = "이 결정 방식을 지닌 당신은 가이드 종족입니다. 자신에게 적합한 환경은 무엇인지에 대해 잘 인식하고 결정을 내릴 때, 당신에게 건강하고 유익할 것입니다. 결정할 것에 대해 믿고 신뢰할 수 있는 주변 사람들과 대화를 나누는 과정을 거치면 좋습니다."
            msg4 = "사람들과의 대화를 통해 결정할 것이 자신에게 적합한지 아닌지, 어떻게 생각하고 있는지 인식할 수 있는 것이죠."
            msg5 = "물론 사람들과 대화를 나눈다고 해서 그들의 의견이나 조언에 따라 결정을 하는 것은 아닙니다. 대화는 단지 결정할 것에 대한 내면의 소리를 꺼내어 들을 수 있게 하는 역할 정도입니다. "
            msg6 = "가능한 내 결정에 유익함을 줄 수 있는 여러 사람과 대화를 해보는 것이 좋습니다."
            tag = "여유를 가지세요,급하면 안돼요"
        elif metadata["a"] == 7:
            h_type = "달 주기 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_7.png"
            msg = "나만의 내부 결정방식을 가지고 있지 않은 당신은 달주기 결정방식을 가지게 됩니다. 달 주기 결정방식이란, 약 한 달에 가까운 28~29일의 시간동안 기다리며 숙고해보는 것을 말합니다. 그러므로 자신만의 고유한 결정방식을 가진 다른 사람들에 비해서 결정을 내릴 때 더 많은 시간을 필요로 합니다."
            msg2 = "빨리 결정을 내리라고 누군가가 재촉할 경우 도무지 뭘 선택해야 할지 몰라서 조바심이 생기거나 불편함을 느꼈을 수 있습니다. 결정을 내릴 때 사용할 수 있는 일관성있는 자신만의 고정된 에너지를 하나도 가지고 있지 않은 당신은, 약 한 달의 기간을 기다리며 그동안 느껴지는 모든 생각변화와 감정변화, 느낌들을 다 느껴보고 결정을 내려야합니다. "
            msg3 = "이 결정 방식을 지닌 당신은 거울종족 입니다. 달의 순환 주기를 따라 변화하는 자신의 모습만이 당신이 유일하게 신뢰할 수 있는 반복적 패턴입니다. 길게 느껴지거나 말이 안된다고도 생각 할 수 있습니다. "
            msg4 = "그러나 당신에게 중요한 결정을 내리기 전, 최소 한 달간 기다리면서 느껴보는 시간을 가지는 것은 매우 중요하며, 동시에 자신이 내려야 하는 결정과 관련된 내용에 대해 당신이 신뢰할 수 있는 주변 사람들과 대화를 나누는 것도 좋습니다."
            msg5 = "이 결정 방식의 핵심은 천천히 기다리며, 무엇보다도 주변의 재촉에 휘둘리지 않는 것입니다. 어느 날 문득, 어떤 자신에게 맞는 결정이 무엇인지 내적 진실을 알게 됩니다. 예를 들어 당신이 무언가 결정을 내려야 하는 날 보름달이 떠있었다면, 그 날로부터 약 한달 뒤 보름달이 뜰 때즈음 어떤 결정이 나있을 것입니다. "
            msg6 = "만일 처음 주어진 초대나 기회가 사라진다면 그것은 처음부터 당신에게 적합한 것이 아닌 것입니다. 당신의 기다림을 함께 기다려주는 사람, 당신의 기다림을 존중해주는 기회가 진정 당신에게 옳은 것이고 놀라움을 가져다 줄 것입니다."
            tag = "여유를 가지세요,달 주기를 따르세요"

        dispatcher.utter_message(
             f'{metadata["pn"]}님, 당신의 결정방식은 {h_type} 이시네요!', image=img)

        #dispatcher.utter_message(json_message = {
        #     "type": "arrContents", "content": [[msg, msg2], [msg3, msg4], [msg5, msg6]], "tags": f'{tag}'})

        dispatcher.utter_message(msg)
        dispatcher.utter_message(msg2)
        dispatcher.utter_message(msg3)
        #dispatcher.utter_message(msg4)
        #dispatcher.utter_message(msg5)
        #dispatcher.utter_message(msg6)
        #dispatcher.utter_message(json_message = {
        #                         "type": "tag", "content": f'{tag}'})

        buttons = []
        buttons.append({"title": f'계속 해주세요', "payload": "/leading_authority_more"})
        buttons.append({"title": f'그만 볼래요', "payload": "/leading_more"})
        
        dispatcher.utter_message(
             f'잘 따라오고 계신가요 ?', buttons=buttons)

        return [SlotSet('step', 2)]

class ActionLeadingAuthorityMore(Action):
    def name(self) -> Text:
        return "action_leading_authority_more"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('action_leading_authority_more')

        metadata = extract_metadata_from_tracker(tracker)

        #dispatcher.utter_message(
        #    f'다음으로 당신의 결정방식에 대해 살펴보겠습니다.')

        if metadata["a"] == 0:
            msg4 = "사온 물건에 대한 감정이 달라진 것입니다. 물론 이런 기분은 한참이 흐르고 나서 느껴질 수도 있습니다. 당신의 감정이 좋을 때에는 무엇이든 ‘Yes’ 하고 허락하기 쉽습니다. 반면에 감정이 안좋을 때에는 ‘No’ 하고 모든게 다 싫고 거부합니다. 그렇기 때문에 순간의 자신의 감정에 따라 무언가를 결정하고 행동하는 것은 만족스럽지 않은 결과로 이어집니다. "
            msg5 = "언제나 감정의 에너지가 높게, 혹은 낮게, 파도를 넘나드는 당신에게, 무엇이 옳은지 진실은 절대 지금 이 순간에 있지 않습니다. 감정의 높고 낮은 파도를 한 번 지나고서 감정이 높지도 낮지도 않은 중간쯤 잠잠해지는 고요한 그 어느 때야 말로 당신이 결정을 할 때입니다. 좋은 감정이나 혹은 나쁜 감정 그 어디에도 치우쳐지지 않은 그때야 말로 무엇이 진실인지 알 수 있는 때인 것입니다. 파도에 올라타 있는 동안에는 내가 지금 높이 올라와 있는지, 혹은 낮게 내려와 있는지 알지 못합니다."
            msg6 = "한 번의 파도가 흘러 지나도록 시간을 들여 바라본다면, 지나간 시간에 나의 감정이 높았는지 낮았는지 알 수 있게 됩니다. 바로 그 고요한 순간에 결정을 하는 것이 당신에게 긍정적 결과를 가져올 것입니다.만약 ‘이렇게 해야지!’하고 마음 먹었는데 어떤 감정의 파도가 일렁이고 있는 중이라면, 아직은 결정할 때가 아닙니다. 자기자신을 조금 더 기다려 줄 필요가 있습니다."
            tag = "감정의 노예,시간이 필요해"
        elif metadata["a"] == 1:
            msg4 = "이 결정 방식은 에너자이저들에게 활력 에너지의 반응을 통해, 무엇이 자신에게 옳고, 어디까지가 자신의 참여 범위인지 등등 내면의 진실을 알 수 있게 해줍니다. 어떤 질문이 들어왔을때 그 질문에 답변하는 그 순간, '예스~' 혹은 '노'라고 느껴지는 결정에 대한 답이 있습니다. 질문을 받았을 때, 활력 에너지를 통한 당신의 몸의 반응은 그 결정이 당신에게 좋은지, 아닌지를 알려 줍니다."
            msg5 = "긍정의 반응이라면, 에너지가 있는, 힘이 넘치는듯 움찔하며 마치 엉덩이가 살짝 들썩이는듯한 느낌을 받을 것입니다. 하지만 부정의 반응이라면 에너지가 없는, 힘이 빠지는 듯~ 마치 몸이 뒤로 물러나는듯한 느낌을 받을 것입니다.이 결정방식을 머리로 이해했다고 하여 한 번에 곧장 몸의 반응으로 연결하여 알아차리기는 힘들 수도 있습니다."
            msg6 = "꾸준하게 자신에게 오는 질문들에서 느껴지는 자신의 몸의 반응을 살피는 연습을 통하여 활력센터의 감각을 되살릴 수 있습니다. 자신에게 주어진 진실이 무엇인지 즉시 알아볼 수 있는 이 놀라운 도구를 적극 사용하길 권합니다."
            tag = "즉각적인 촉,Yes or No"            
        elif metadata["a"] == 2:
            msg4 = "결정은 반드시 지금, 이 순간에 내려지는 것입니다. 잠시라도 주저한다면 직관은 사라질 것입니다."
            msg5 = "직관은 미래에 대해 알지 못합니다. ‘10분만, 한 시간 뒤에, 하루만 있다가’ 하면서 그 순간을 지나친다면, 결정은 바뀔 수 있습니다. 어떤 것이 자신에게 안전하다면 본능적으로 지금, 이 순간에 바로 알게 될 것입니다. 반대로 자신에게 해롭거나 위험한 것도 똑같이 알 수 있습니다. "
            msg6 = "힘들겠지만 당신이 맞는 결정을 하기 위해서는 자신의 직관의 신호를 신뢰해야 합니다."
            tag = "생존 본능을 따라,주저하지 말 것"
        elif metadata["a"] == 3:
            msg4 = "당신은 의지력을 발휘하여 약속을 만들고, 그것을 지킬 때 건강합니다. 하지만 의지력은 한계가 있으니 일과 휴식의 균형을 가지고 있어야 하겠죠. 에고센터와 관련이 있는 장기는 바로 심장인데, 심장에 큰 부담을 주지 않기 위해서는 어떤 장기적인 일을 시작할 때에는 반드시 그것이 자신에게 옳은 일인지 확인한 후에 결정해야 합니다."
            msg5 = "그릇된 결정은 심장에 과부하를 주면서까지 그 약속을 이행하기 위해 몸을 혹사시킬 것입니다."
            msg6 = "일을 한만큼 휴식하고 노는 시간을 가져야합니다. 이 균형을 유지하는 것은 에너지적으로도, 육체적으로도 필수입니다."
            tag = "내 안의 소리가 들려,나 중심의 선택"
        elif metadata["a"] == 4:
            msg4 = "무엇이 나에게 기쁨을 주는지, 무엇이 나를 나 답게 느끼게 하는지에 따라 결정하는 사람입니다. "
            msg5 = "스스로에게 소리내어 질문을 던져보세요. ‘이 결정을 하면 나는 행복할까? 이것을 통해 나를 표현할 수 있을까? 이게 나에게 맞는 방향 일까?’ 결정을 하기 전, 주변 사람들과 대화를 나누며 자신이 결정할 것에 대해 어떻게 말하고 있는지 들어보는 것은 매우 도움이 됩니다. "
            msg6 = "되도록 여러 사람과 대화를 해보는 것이 좋습니다. 또한 자기 자신의 말을 들어보는 것을 통해 나를 위해 옳은 방향이 무엇인지 알 수 있습니다."
            tag = "나를 위한 선택,주변 사람들과 대화"
        elif metadata["a"] == 5:
            msg4 = "에고센터는 실제로 심장건강과 관련이 있는데, 에고센터가 정의된 사람들은 약속을 만들고, 그 약속을 지키고자 의지를 만들어서 쓰고, 정말로 그 약속을 지켜낼 때 건강합니다. "
            msg5 = "심장에 부담을 주지 않기 위해서는, 어떤 장기적인 일을 시작할 때에는 반드시 그것이 자신에게 옳은 일인지 확인한 후에 결정해야 합니다. "
            msg6 = "일한 만큼 휴식하고 노는 시간을 가져야합니다. 이 균형을 유지하는 것은 에너지적으로도, 육체적으로도 필수입니다."
            tag = "주변 환경의 영향,대화가 필요해"
        elif metadata["a"] == 6:
            msg4 = "사람들과의 대화를 통해 결정할 것이 자신에게 적합한지 아닌지, 어떻게 생각하고 있는지 인식할 수 있는 것이죠."
            msg5 = "물론 사람들과 대화를 나눈다고 해서 그들의 의견이나 조언에 따라 결정을 하는 것은 아닙니다. 대화는 단지 결정할 것에 대한 내면의 소리를 꺼내어 들을 수 있게 하는 역할 정도입니다. "
            msg6 = "가능한 내 결정에 유익함을 줄 수 있는 여러 사람과 대화를 해보는 것이 좋습니다."
            tag = "여유를 가지세요,급하면 안돼요"
        elif metadata["a"] == 7:
            msg4 = "그러나 당신에게 중요한 결정을 내리기 전, 최소 한 달간 기다리면서 느껴보는 시간을 가지는 것은 매우 중요하며, 동시에 자신이 내려야 하는 결정과 관련된 내용에 대해 당신이 신뢰할 수 있는 주변 사람들과 대화를 나누는 것도 좋습니다."
            msg5 = "이 결정 방식의 핵심은 천천히 기다리며, 무엇보다도 주변의 재촉에 휘둘리지 않는 것입니다. 어느 날 문득, 어떤 자신에게 맞는 결정이 무엇인지 내적 진실을 알게 됩니다. 예를 들어 당신이 무언가 결정을 내려야 하는 날 보름달이 떠있었다면, 그 날로부터 약 한달 뒤 보름달이 뜰 때즈음 어떤 결정이 나있을 것입니다. "
            msg6 = "만일 처음 주어진 초대나 기회가 사라진다면 그것은 처음부터 당신에게 적합한 것이 아닌 것입니다. 당신의 기다림을 함께 기다려주는 사람, 당신의 기다림을 존중해주는 기회가 진정 당신에게 옳은 것이고 놀라움을 가져다 줄 것입니다."
            tag = "여유를 가지세요,달 주기를 따르세요"

        dispatcher.utter_message(msg4)
        dispatcher.utter_message(msg5)
        dispatcher.utter_message(msg6)
        dispatcher.utter_message(json_message = {
                                 "type": "tag", 'sender':metadata['uID'], "content": f'{tag}', "guide": f'설명을 좀 더 쉽고 간결하게 이해할 수 있도록 {metadata["pn"]}님의 성향을 태그로 보여드릴게요.'})

        buttons = []
        buttons.append({"title": f'아니오, 설명해주세요', "payload": "/authority_common_mean"})
        buttons.append({"title": f'알고 있어요, 다음 설명 듣고 싶어요!', "payload": "/leading_centers"})
        buttons.append({"title": f'이 항목 말고 다른 설명을 듣고 싶어요', "payload": "/leading_more"})

        dispatcher.utter_message(
             f'추가로 결정방식에는 8가지 방식이 있는 것을 알고 계신가요?', buttons=buttons)

        return [SlotSet('step', 2)]        

class ActionGetHumanDesignAuthority(Action):
    def name(self) -> Text:
        return "action_get_humandesign_authority"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']

        metadata = extract_metadata_from_tracker(tracker)

        for i in range(len(entities)):
            h_authority = (entities[i]['value'])

        h_type = None

        if h_authority == 'authority-0':
            h_type = "감정 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_0.png"
            msg = "지금 당신의 기분은 어떤가요? 좋은가요? 나쁜가요? 기쁜가요? 슬픈가요? 당신이 느끼고 있는 감정이 무엇이든지 '지금 이 순간'에는 당신에게 무엇을 결정 할 만한 때가 아닙니다. 지금 이 순간에는 기분이 좋다가도 금방 나빠지기도 하고, 또 다음 순간에는 기쁘다가도 슬퍼질 수 있는 것이 바로 감정입니다."
            msg2 = "당신은 이렇게 시시각각 변화하는 다양한 감정을 가지고 있는 사람입니다. 이렇게 지속적으로 감정이 영향을 미치고 있는 지금 이 순간에 곧바로 결정을 내릴 경우, 그 결과는 몹시도 불만족스러울 수 있습니다. 자신의 감정이 어떤지는 스스로 잘 알고 있을 수도 모를 수도 있지만, 분명한 것은 당신의 감정은 늘 파도가 치는 것처럼 위 아래로 움직이고, 무드가 좋았다가 나빴다가 하는 움직임 속에 있다는 것입니다."
            msg3 = "한 순간 기분이 좋아서 흔쾌히 결정을 내렸을 때, 혹은 기분이 안좋아서 결정을 보류하고 미뤘다가 기회를 놓쳤을 때. 양 쪽 모두 결국에는 후회스러울 수 있습니다. 당신이 결정을 내리던 그때의 그 감정, 그 기분은 이미 파도처럼 지나간 순간이기 때문입니다. 예를 들어 쇼핑을 하고 나서 후회하는 일은 일상입니다. ’아무래도 이건 아닌것 같아. 바꿔야겠어. 환불 해야겠어…’ 하고 마음이 바뀌는건 너무나 흔한 일입니다. 밖에서 물건을 사던 때의 기분은 이미 지나가고, 집에 돌아왔을 때에는 감정이 새롭게 변했기 때문입니다. "
            msg4 = "사온 물건에 대한 감정이 달라진 것입니다. 물론 이런 기분은 한참이 흐르고 나서 느껴질 수도 있습니다. 당신의 감정이 좋을 때에는 무엇이든 ‘Yes’ 하고 허락하기 쉽습니다. 반면에 감정이 안좋을 때에는 ‘No’ 하고 모든게 다 싫고 거부합니다. 그렇기 때문에 순간의 자신의 감정에 따라 무언가를 결정하고 행동하는 것은 만족스럽지 않은 결과로 이어집니다. "
            msg5 = "언제나 감정의 에너지가 높게, 혹은 낮게, 파도를 넘나드는 당신에게, 무엇이 옳은지 진실은 절대 지금 이 순간에 있지 않습니다. 감정의 높고 낮은 파도를 한 번 지나고서 감정이 높지도 낮지도 않은 중간쯤 잠잠해지는 고요한 그 어느 때야 말로 당신이 결정을 할 때입니다. 좋은 감정이나 혹은 나쁜 감정 그 어디에도 치우쳐지지 않은 그때야 말로 무엇이 진실인지 알 수 있는 때인 것입니다. 파도에 올라타 있는 동안에는 내가 지금 높이 올라와 있는지, 혹은 낮게 내려와 있는지 알지 못합니다."
            msg6 = "한 번의 파도가 흘러 지나도록 시간을 들여 바라본다면, 지나간 시간에 나의 감정이 높았는지 낮았는지 알 수 있게 됩니다. 바로 그 고요한 순간에 결정을 하는 것이 당신에게 긍정적 결과를 가져올 것입니다.만약 ‘이렇게 해야지!’하고 마음 먹었는데 어떤 감정의 파도가 일렁이고 있는 중이라면, 아직은 결정할 때가 아닙니다. 자기자신을 조금 더 기다려 줄 필요가 있습니다."
            tag = "감정의 노예,시간이 필요해"
        elif h_authority == 'authority-1':
            h_type = "활력 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_1.png"
            msg = "에너지(활력)가 있는지 없는지에 따라 결정하는 것이 당신에게 맞는 결정방식입니다. 에너지가 있는지 없는지라는 것은 생각이 아닌 몸으로 느낄 수 있는 느낌인데 “뭔가 움찔하듯” 몸에서 솟아나는 반응을 말하는 것 입니다."
            msg2 = "이 결정 방식을 지닌 당신은 에너자이저 종족 또는 스피드 에너자이저 종족입니다."
            msg3 = "이 반응은 “응! 어!” 또는 ”흠...” “아니.” 등의 소리와 비슷한 느낌이며, 동시에 몸이 약간이라도 스프링처럼 튀어오르는 듯한 활력에너지의 반응은 에너자이저 종족들에게 질문이 던져 졌을 때, 즉각적으로 몸에서 느껴지는 것입니다. 당신에게 결정할 것에 대한 질문이 던져 졌을 때, 주저함이 느껴진다면(애매모호할 때), “지금은 잘 모르겠네~ 나중에 다시 질문해줄래요?” 가 정답입니다."
            msg4 = "이 결정 방식은 에너자이저들에게 활력 에너지의 반응을 통해, 무엇이 자신에게 옳고, 어디까지가 자신의 참여 범위인지 등등 내면의 진실을 알 수 있게 해줍니다. 어떤 질문이 들어왔을때 그 질문에 답변하는 그 순간, '예스~' 혹은 '노'라고 느껴지는 결정에 대한 답이 있습니다. 질문을 받았을 때, 활력 에너지를 통한 당신의 몸의 반응은 그 결정이 당신에게 좋은지, 아닌지를 알려 줍니다."
            msg5 = "긍정의 반응이라면, 에너지가 있는, 힘이 넘치는듯 움찔하며 마치 엉덩이가 살짝 들썩이는듯한 느낌을 받을 것입니다. 하지만 부정의 반응이라면 에너지가 없는, 힘이 빠지는 듯~ 마치 몸이 뒤로 물러나는듯한 느낌을 받을 것입니다.이 결정방식을 머리로 이해했다고 하여 한 번에 곧장 몸의 반응으로 연결하여 알아차리기는 힘들 수도 있습니다."
            msg6 = "꾸준하게 자신에게 오는 질문들에서 느껴지는 자신의 몸의 반응을 살피는 연습을 통하여 활력센터의 감각을 되살릴 수 있습니다. 자신에게 주어진 진실이 무엇인지 즉시 알아볼 수 있는 이 놀라운 도구를 적극 사용하길 권합니다."
            tag = "즉각적인 촉,Yes or No"            
        elif h_authority == 'authority-2':
            h_type = "직관 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_2.png"
            msg = "섬세하게 찾아오는 순간의 직관에 따라 결정을 했을 때 당신의 몸은 안전할 수 있습니다. 직관은 어떤 사람이나 무언가에 대해서 아주 즉각적인 공명이나 인식을 느끼는 것이며, 당신은 그 사람이나 무언가가 안전한지 아닌지를 구별하는 것입니다."
            msg2 = "당신은 미묘한 변화를 민감하게 느껴야 하며, 언제라도 그 직관(섬세한 느낌)을 믿고 삶을 움직일 수 있어야 합니다. 이러한 직관의 신호는 아주 작게 전달되며 단 한 번의 기회 뿐입니다. "
            msg3 = "외부로부터 오는 여러 압박이나 생각으로 인해 직관을 무시하고 고민하며 계산하거나 의심한다면, 당신은 위험에 처할 수 있습니다. 오랜 시간을 심사숙고하여 결정하는 것은 당신에게 맞지 않습니다. "
            msg4 = "결정은 반드시 지금, 이 순간에 내려지는 것입니다. 잠시라도 주저한다면 직관은 사라질 것입니다."
            msg5 = "직관은 미래에 대해 알지 못합니다. ‘10분만, 한 시간 뒤에, 하루만 있다가’ 하면서 그 순간을 지나친다면, 결정은 바뀔 수 있습니다. 어떤 것이 자신에게 안전하다면 본능적으로 지금, 이 순간에 바로 알게 될 것입니다. 반대로 자신에게 해롭거나 위험한 것도 똑같이 알 수 있습니다. "
            msg6 = "힘들겠지만 당신이 맞는 결정을 하기 위해서는 자신의 직관의 신호를 신뢰해야 합니다."
            tag = "생존 본능을 따라,주저하지 말 것"
        elif h_authority == 'authority-3':
            h_type = "에고현시 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_3.png"
            msg = "혁신주도가의 에고현시 결정 방식은 “나 이거 할거야. 나 할 수 있어. 나 하는 사람이야. 내가 이것도 못할 것 같아?” 등등. 자신이 어떤 결정을 원하는지 알기 위해 자신이 하는 말을 스스로 잘 들어봐야 합니다."
            msg2 = "머리 속에 떠오르는 생각이 아닌, 입을 통해 밖으로 표현되는 자신이 말을 직접 들어보고 결정해야 합니다."
            msg3 = "당신은 자신이 한 말 속에 무엇을 어떻게 결정할지 진실이 담겨있습니다. 주변 사람들에게 말로 표현을 함으로서 자신의 의지를 표현함과 동시에 자신의 결정을 알리는 것입니다. 그것이 삶을 이끌고 새로운 것을 시작하게 할 것입니다."
            msg4 = "당신은 의지력을 발휘하여 약속을 만들고, 그것을 지킬 때 건강합니다. 하지만 의지력은 한계가 있으니 일과 휴식의 균형을 가지고 있어야 하겠죠. 에고센터와 관련이 있는 장기는 바로 심장인데, 심장에 큰 부담을 주지 않기 위해서는 어떤 장기적인 일을 시작할 때에는 반드시 그것이 자신에게 옳은 일인지 확인한 후에 결정해야 합니다."
            msg5 = "그릇된 결정은 심장에 과부하를 주면서까지 그 약속을 이행하기 위해 몸을 혹사시킬 것입니다."
            msg6 = "일을 한만큼 휴식하고 노는 시간을 가져야합니다. 이 균형을 유지하는 것은 에너지적으로도, 육체적으로도 필수입니다."
            tag = "내 안의 소리가 들려,나 중심의 선택"
        elif h_authority == 'authority-4':
            h_type = "방향성 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_4.png"
            msg = "결정해야 할 무언가에 대해 자신이 무슨 말을 하는지 들어보는 과정을 거치는 것이 당신의 결정 방식입니다. 이 결정 방식을 지닌 당신은 가이드 종족인데요. "
            msg2 = "다른 사람이나 세상으로부터 초대를 받았을 때 생겨나는 반응 속에 당신이 알아야 하는 모든 것이 들어 있습니다. 자신에게 맞는 결정에 대한 진실은 항상 정체성을 통해 표현됩니다."
            msg3 = "결정할 것에 대한 표현에 자신을 위한 무언가가 담겨있지 않다면, 거기에는 당신을 위한 성공은 없습니다. 초대가 온 것에 대해 자신이 하는 말을 들어보세요."
            msg4 = "무엇이 나에게 기쁨을 주는지, 무엇이 나를 나 답게 느끼게 하는지에 따라 결정하는 사람입니다. "
            msg5 = "스스로에게 소리내어 질문을 던져보세요. ‘이 결정을 하면 나는 행복할까? 이것을 통해 나를 표현할 수 있을까? 이게 나에게 맞는 방향 일까?’ 결정을 하기 전, 주변 사람들과 대화를 나누며 자신이 결정할 것에 대해 어떻게 말하고 있는지 들어보는 것은 매우 도움이 됩니다. "
            msg6 = "되도록 여러 사람과 대화를 해보는 것이 좋습니다. 또한 자기 자신의 말을 들어보는 것을 통해 나를 위해 옳은 방향이 무엇인지 알 수 있습니다."
            tag = "나를 위한 선택,주변 사람들과 대화"
        elif h_authority == 'authority-5':
            h_type = "에고투사 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_5.png"
            msg = "가이드 종족의 에고투사 결정방식은 “내가 원하는게 뭘까? 나를 위한 것이 뭐가 있을까? 내가 그것을 할 수 있을까?“ 하는 자신을 위한 질문을 스스로에게 던져봐야 합니다. 당신은 스스로 묻고 답하는 시간을 통해 '이건 좋은 것 같아' 하는 의지력을 느끼거나, 혹은 어떤 의지도 느끼지 못할 것입니다."
            msg2 = "특히 가이드 종족인 당신은, 다른 사람이나 세상으로부터 자신의 능력을 인정받고, 우리와 함께 하자고 초대를 기다려야 합니다. 어떤 초대가 왔을 때에는, 그 초대를 받아들일지 아닌지에 대해 스스로 질문을 던져보며 자신에게 의지력이 생기는지 안생기는지 살펴보고 결정해야 합니다. "
            msg3 = "의지력이 있고/없고가 당신의 결정에 주요하게 작용합니다. 당신은 의지력을 발휘하여 약속을 만들고, 그것을 지킬 때 건강합니다. 이러한 의지력에는 한계가 있기에, 늘 일과 휴식의 균형을 잊지 말아야 합니다."
            msg4 = "에고센터는 실제로 심장건강과 관련이 있는데, 에고센터가 정의된 사람들은 약속을 만들고, 그 약속을 지키고자 의지를 만들어서 쓰고, 정말로 그 약속을 지켜낼 때 건강합니다. "
            msg5 = "심장에 부담을 주지 않기 위해서는, 어떤 장기적인 일을 시작할 때에는 반드시 그것이 자신에게 옳은 일인지 확인한 후에 결정해야 합니다. "
            msg6 = "일한 만큼 휴식하고 노는 시간을 가져야합니다. 이 균형을 유지하는 것은 에너지적으로도, 육체적으로도 필수입니다."
            tag = "주변 환경의 영향,대화가 필요해"
        elif h_authority == 'authority-6':
            h_type = "외부환경 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_6.png"
            msg = "나만의 내부 결정방식을 가지고 있지 않은 당신은 외부환경 결정방식을 가지게 됩니다.자신만의 고유한 결정방식을 가진 다른 사람들에 비해서 결정을 내릴 때 더 많은 시간을 필요로 합니다. 빨리 결정을 내리라고 누군가가 재촉할 경우 도무지 뭘 선택해야 할지 몰라서 조바심이 생기거나 불편함을 느꼈을 수 있습니다."
            msg2 = "자신을 둘러싼 다른 사람이나 다른 무언가 등등, 주변 환경의 느낌이 썩 좋지 않다면, 그것에서 만들어지는 협상, 주고받는 아이디어들 역시 좋을 리 없습니다. 당신이 스스로에게 가장 먼저 던져봐야 하는 질문은 ‘지금 이 환경이 나에게 적합한가? 내가 지금 좋은 환경에 있나?’ 입니다."
            msg3 = "이 결정 방식을 지닌 당신은 가이드 종족입니다. 자신에게 적합한 환경은 무엇인지에 대해 잘 인식하고 결정을 내릴 때, 당신에게 건강하고 유익할 것입니다. 결정할 것에 대해 믿고 신뢰할 수 있는 주변 사람들과 대화를 나누는 과정을 거치면 좋습니다."
            msg4 = "사람들과의 대화를 통해 결정할 것이 자신에게 적합한지 아닌지, 어떻게 생각하고 있는지 인식할 수 있는 것이죠."
            msg5 = "물론 사람들과 대화를 나눈다고 해서 그들의 의견이나 조언에 따라 결정을 하는 것은 아닙니다. 대화는 단지 결정할 것에 대한 내면의 소리를 꺼내어 들을 수 있게 하는 역할 정도입니다. "
            msg6 = "가능한 내 결정에 유익함을 줄 수 있는 여러 사람과 대화를 해보는 것이 좋습니다."
            tag = "여유를 가지세요,급하면 안돼요"
        elif h_authority == 'authority-7':
            h_type = "달 주기 결정방식"
            img = "https://asset.i-manual.co.kr/static/images/profile/authority/authority_7.png"
            msg = "나만의 내부 결정방식을 가지고 있지 않은 당신은 달주기 결정방식을 가지게 됩니다. 달 주기 결정방식이란, 약 한 달에 가까운 28~29일의 시간동안 기다리며 숙고해보는 것을 말합니다. 그러므로 자신만의 고유한 결정방식을 가진 다른 사람들에 비해서 결정을 내릴 때 더 많은 시간을 필요로 합니다."
            msg2 = "빨리 결정을 내리라고 누군가가 재촉할 경우 도무지 뭘 선택해야 할지 몰라서 조바심이 생기거나 불편함을 느꼈을 수 있습니다. 결정을 내릴 때 사용할 수 있는 일관성있는 자신만의 고정된 에너지를 하나도 가지고 있지 않은 당신은, 약 한 달의 기간을 기다리며 그동안 느껴지는 모든 생각변화와 감정변화, 느낌들을 다 느껴보고 결정을 내려야합니다. "
            msg3 = "이 결정 방식을 지닌 당신은 거울종족 입니다. 달의 순환 주기를 따라 변화하는 자신의 모습만이 당신이 유일하게 신뢰할 수 있는 반복적 패턴입니다. 길게 느껴지거나 말이 안된다고도 생각 할 수 있습니다. "
            msg4 = "그러나 당신에게 중요한 결정을 내리기 전, 최소 한 달간 기다리면서 느껴보는 시간을 가지는 것은 매우 중요하며, 동시에 자신이 내려야 하는 결정과 관련된 내용에 대해 당신이 신뢰할 수 있는 주변 사람들과 대화를 나누는 것도 좋습니다."
            msg5 = "이 결정 방식의 핵심은 천천히 기다리며, 무엇보다도 주변의 재촉에 휘둘리지 않는 것입니다. 어느 날 문득, 어떤 자신에게 맞는 결정이 무엇인지 내적 진실을 알게 됩니다. 예를 들어 당신이 무언가 결정을 내려야 하는 날 보름달이 떠있었다면, 그 날로부터 약 한달 뒤 보름달이 뜰 때즈음 어떤 결정이 나있을 것입니다. "
            msg6 = "만일 처음 주어진 초대나 기회가 사라진다면 그것은 처음부터 당신에게 적합한 것이 아닌 것입니다. 당신의 기다림을 함께 기다려주는 사람, 당신의 기다림을 존중해주는 기회가 진정 당신에게 옳은 것이고 놀라움을 가져다 줄 것입니다."
            tag = "여유를 가지세요,달 주기를 따르세요"

        if h_type is not None:
            dispatcher.utter_message(f'"{h_type}"에 대해 설명드릴께요', image=img)
            dispatcher.utter_message(msg)
            dispatcher.utter_message(msg2)
            dispatcher.utter_message(msg3)
            dispatcher.utter_message(msg4)
            dispatcher.utter_message(msg5)
        else:
            dispatcher.utter_message('찾고자 하는 결정방식을 저희가 찾지 못했어요. 다시 한번 확인하시어 입력해주세요')
            dispatcher.utter_message(json_message = {
                "type": "tag", 'sender':metadata['uID'], "content": f'감정 결정방식,활력 결정방식,직관 결정방식,에고현시 결정방식,방향성 결정방식,에고투사 결정방식,외부환경 결정방식,달 주기 결정방식', "guide": f'검색 가능한 결정방식을 태그로 보여드릴게요.'})     

        buttons = []
        buttons.append({"title": f'네. 이어서 나의 센터에 대해 알아볼래요', "payload": "/leading_centers"})
        buttons.append({"title": f'다른 결정방식도 알아보고 싶어요', "payload": "/authority_common_mean"})

        dispatcher.utter_message(
            f'궁금하신 내용은 찾으셨나요?', buttons=buttons)
        
        # dispatcher.utter_message("로케이션 세팅 완료!")
        return []

class ActionGetHumanDesignCommonAuthority(Action):
    def name(self) -> Text:
        return "action_get_humandesign_common_authority"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # {
        #     "title": "Link name",
        #     "url": "http://link.url",
        #     "type": "web_url"
        # },

        metadata = extract_metadata_from_tracker(tracker)
        print("MetaData: ", metadata)

        dispatcher.utter_message(
            "각각의 종족에는 종족에 맞는 의사결정을 내리는 방식이 있습니다. 이는 스스로 당신의 삶을 이끌 수 있는 의사결정방식 체계입니다.")

        retVal = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "감정 결정방식",
                        "subtitle": "감정의 노예,시간이 필요해",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_0.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "감정 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "활력 결정방식",
                        "subtitle": "즉각적인 촉,Yes or No",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_1.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "활력 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "직관 결정방식",
                        "subtitle": "생존 본능을 따라,주저하지 말 것",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_2.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "직관 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "에고현시 결정방식",
                        "subtitle": "내 안의 소리가 들려,나 중심의 선택",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_3.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "에고현시 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "방향성 결정방식",
                        "subtitle": "나를 위한 선택,주변 사람들과 대화",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_4.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "방향성 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "에고투사 결정방식",
                        "subtitle": "주변 환경의 영향,대화가 필요해",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_5.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "에고투사 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "외부환경 결정방식",
                        "subtitle": "여유를 가지세요,급하면 안돼요",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_6.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "외부환경 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                    {
                        "title": "달 주기 결정방식",
                        "subtitle": "여유를 가지세요,달 주기를 따르세요",
                        "image_url": "https://asset.i-manual.co.kr/static/images/profile/authority/authority_7.png",
                        "buttons": [
                            {
                                "title": "자세히",
                                "type": "postback",
                                "payload": "달 주기 결정방식이란 무엇인가요?"
                            }
                        ]
                    },
                ]
            }
        }
        dispatcher.utter_message(
            text="각 결정방식에 대해 궁금하시면 아래 자세히 버튼을 눌러보세요", attachment=retVal)
        
        print("get Step")
        print(tracker.get_slot('step'))
        print("get Step end")

        buttons = []
        buttons.append({"title": f'센터 알아보기', "payload": "/leading_centers"})
        buttons.append({"title": f'이 항목 말고 다른 설명을 듣고 싶어요', "payload": "/leading_more"})

        dispatcher.utter_message(
             f'이어서 나의 센터에 대해 알아보실래요?', buttons=buttons)
        #dispatcher.utter_message(json_message={'type': 'continue', 'value': tracker.get_slot('step')})
        # dispatcher.utter_message("로케이션 세팅 완료!")
        return []        
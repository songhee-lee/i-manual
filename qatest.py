from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import AutoConfig
import torch
import argparse

class QuestionAnswering():
    """I-manual question answering class.
    Attributes:
        model (AutoModelForQuestionAnswering): transformers model.
        tokenizer (AutoTokenizer): transformers tokenizer.
        pipeline (QuestionAnsweringPipeline): transformers pipeline.
    """

    def __init__(self, pretrained_model_name_or_path=None):
        """Inits QuestionAnswering, and load a pre-trained model.

         Args:
            pretrained_model_name_or_path (str):
                Pretrained huggingface model name or model path.
        """

        self.config = AutoConfig.from_pretrained(
            pretrained_model_name_or_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(
            pretrained_model_name_or_path,
            config=self.config)
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path)

    def __call__(self, question, context):
        """Returns answer(s) for given question, context.
        Args:
            question: question of interest.
            context: context where appropriate answer can be found.
        Returns:
            A dictionary containing answer and other informations.
        """

        inputs = self.tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]

        text_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        answer_start_scores, answer_end_scores = self.model(**inputs, return_dict=False)

        answer_start = torch.argmax(answer_start_scores)  # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
        
        answer = self.tokenizer.convert_tokens_to_string(self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

        return { "question" : question,
                 "answer" : answer,
                 "input_ids" : input_ids,
                 "answer_start_scores" : answer_start_scores,
                 "answer_end_scores" : answer_end_scores,
                 }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        default=None,
        type=str,
        required=True
    )


    args = parser.parse_args()


    context = r"""전략은 각자의 바디그래프에 맞게 흐르는 독특한 에너지의 디자인을 이해하고, 저항을 받지 않고 제대로 작동되도록 사는 방법을 말합니다.
    전략은 다른 사람들과 비교하는 버릇을 깨고 스스로의 독특함을 발견하여, 자기 자신의 모습 그대로를 그냥 즐길 수 있게 합니다.
    전략을 알면 진정한 자기 모습을 찾는 과정에 도움이 됩니다. 자신의 전략에 맞추어 사는 것이 개인적 실험의 시작입니다.
    스스로 전략을 실험해 그것이 옳은지 알아보세요.
    자신의 전략과 결정권을 사용해 자기 자신이 아닌 세상 밖의 권위에 맹목적으로 의존하는 버릇을 바꾸기 시작해봐요."""

    questions = [
        "전략이란 무엇인가요?",
        "전략을 왜 알려주나요?",
        "전략을 왜 따라야 하나요?",
        "전략을 알면 무엇이 좋은가요?",
        ]


    qa = QuestionAnswering(args.model_name_or_path)

    for question in questions:
        answer = qa(question=question, context=context)
        print(f"Question: {answer['question']}")
        print(f"Answer: {answer['answer']}\n")
        
if __name__ == "__main__":
    main()

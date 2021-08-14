from transformers import AutoTokenizer, AutoModelForQeustionAnswering
from transformers import QuestionAnsweringPipeline

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
        self.model = AutoModelForQuestionAnswering.from_pretrained(
            pretrained_model_name_or_path)
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path)

        self.pipeline =  QuestionAnsweringPipeline(self.model, self.tokenizer)

    def __call__(self, question, context):
        """Returns answer(s) for given question, context.
        Args:
            question: question of interest.
            context: context where appropriate answer can be found.
        Returns:
            A dictionary containing answer and other informations.
        """
        answer = self.pipeline(question=question, context=context)

        return answer

from model.response_emotion_extration.Interface.IResponseEmotionExtraction import IResponseTextExtraction
from model.response_emotion_extration.ResponseEmotionExtraction import ResponseEmotionExtraction
from model.response_emotion_extration.AWSStrategy import AWSStrategy


class ResponseEmotionExtractionFactory:

    def __new__(cls):
        if not hasattr(cls, "_inst"):
            cls._inst = super(ResponseEmotionExtractionFactory, cls).__new__(cls)
        return cls._inst


    def get_emotion_extraction_object(self, strategy: str = None) -> IResponseTextExtraction:
        """
        This method allows to build a concrete instance of IResponseTextExtraction
        :param strategy: Strategy that you want to use for emotion extraction. E.g. if you have an AWS response you can pass aws
        :return: A concrete instance of IResponseTextExtraction
        """
        # TODO qui si può inserire del codice che permette di capire dinamicamente di che tipo di response è.
        if strategy is None:
            print("Strategy for emotion extraction does not specified, i use the default one.")
            emotion_extraction_object = ResponseEmotionExtraction(AWSStrategy())
        elif str(strategy).lower() == "aws":
            print("Selected strategy AWS for emotion extraction.")
            emotion_extraction_object = ResponseEmotionExtraction(AWSStrategy())
        else:
            print("Can't find given strategy for emotion extraction, i use the default one.")
            emotion_extraction_object = ResponseEmotionExtraction(AWSStrategy())
        return emotion_extraction_object

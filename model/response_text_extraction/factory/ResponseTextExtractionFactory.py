from model.response_text_extraction.Interface.IResponseTextExtraction import IResponseTextExtraction
from model.response_text_extraction.ResponseTextExtraction import ResponseTextExtraction
from model.response_text_extraction.StrategyA import StrategyA


class ResponseTextExtractionFactory:

    def __new__(cls):
        if not hasattr(cls, "_inst"):
            cls._inst = super(ResponseTextExtractionFactory, cls).__new__(cls)
        return cls._inst


    def get_text_extraction_object(self, strategy: str = None) -> IResponseTextExtraction:
        """
        This method builds a concrete instance of IResponseTextExtraction
        :param strategy: Strategy to use. If you don't specify anything or you specify an unknown strategy, default strategy is used
        :return: Concrete instance of IResponseTextExtraction
        """
        # TODO qui si può inserire del codice che permette di capire dinamicamente di che tipo di response è.
        if strategy is None:
            print("Strategy for text extraction does not specified, i use the default one.")
            text_extraction_object = ResponseTextExtraction(StrategyA())
        elif str(strategy).lower() == "a":
            print("Selected strategy A for text extraction.")
            text_extraction_object = ResponseTextExtraction(StrategyA())
        else:
            print("Can't find given strategy for text extraction, i use the default one.")
            text_extraction_object = ResponseTextExtraction(StrategyA())
        return text_extraction_object

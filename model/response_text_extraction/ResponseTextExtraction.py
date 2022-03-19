from model.response_text_extraction.Interface.IResponseTextExtraction import IResponseTextExtraction


class ResponseTextExtraction(IResponseTextExtraction):

    def __init__(self, response_text_extraction_strategy: IResponseTextExtraction):
        self.__response_text_extraction_strategy = response_text_extraction_strategy

    def extract_text(self, data: dict) -> str:
        """
        Questa funzione estrae da un dizionario contenente una trascrizione, il testo.
        :param data: Dizionario contenente le informazioni di trascrizione.
        :return: Testo della trascrizione
        """
        return self.__response_text_extraction_strategy.extract_text(data)

    def extract_time_from_transcription(self, words_list: list, data: dict) -> dict:
        """
        Questa funzione estrae gli start e end time delle parole fornite.
        :param words_list: Parole da cercare
        :param data: Response del servizio di trascrizione
        :return: dizionario contenente start e end time delle parole
        """
        return self.__response_text_extraction_strategy.extract_time_from_transcription(words_list, data)

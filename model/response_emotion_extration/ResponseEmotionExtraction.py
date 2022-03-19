from model.response_emotion_extration.Interface.IResponseEmotionExtraction import IResponseTextExtraction


class ResponseEmotionExtraction(IResponseTextExtraction):

    def __init__(self, concrete_strategy: IResponseTextExtraction):
        self.__concrete_strategy = concrete_strategy

    def extract_emotion_by_time(self, response: list, time: int, negative_gap: int = 0, positive_gap: int = 0,
                                step_size: int = 500, verbose: bool = False) -> (str, int):
        """
        Questa funzione permette di estrarre le emozioni da una risposta di un generico servizio tra quelli supportati, piu vicino possibile ad un istante dato.
        :param response: Lista di emozioni
        :param time: Tempo (in ms) da quale estrarre l'emozione
        :param negative_gap: Delta nel quale cercare l'emozione (precedente a time). Se < 0 il limite sinistro viene impostato a 0.
        :param positive_gap: Delta nel quale cercare l'emozione (successivo a time). Se < 0 il limite destro viene impostato all'ultimo istante della lista fornita.
        :param step_size: Step incrementale per la ricerca del'emozione.
        :param verbose: Flag di verbosity
        :return: Tupla contenente l'emozione e il timestamp
        """
        return self.__concrete_strategy.extract_emotion_by_time(response, time, negative_gap, positive_gap, step_size, verbose)

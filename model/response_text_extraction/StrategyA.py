from model.response_text_extraction.Interface.IResponseTextExtraction import IResponseTextExtraction


class StrategyA(IResponseTextExtraction):

    def __init__(self):
        pass

    def extract_text(self, data: dict) -> str:
        """
        Questa funzione estrae da un dizionario di risposta dal servizio A contenente una trascrizione, il testo.
        :param data: Dizionario contenente le informazioni di trascrizione.
        :return: Testo della trascrizione
        """
        text = data.get("results", {}).get("transcripts", [])
        extracted_text = ""
        if type(text) is list and len(text) > 0:
            text = text[0]
            if type(text) is dict:
                extracted_text = text.get("transcript", "")
        return extracted_text

    def extract_time_from_transcription(self, words_list: list, data: dict) -> dict:
        """
        Questa funzione estrae gli start e end time delle parole fornite.
        :param words_list: Parole da cercare
        :param data: Response del servizio di trascrizione A
        :return: dizionario contenente start e end time delle parole
        """
        words_info = {}
        items = data.get("results", {}).get("items", [])
        words_list = [word_tuple[0] for word_tuple in words_list]
        for word in words_list:
            words_info[word] = []
            for sub_dict in items:
                if type(sub_dict.get('alternatives', [])) is list and len(sub_dict.get('alternatives', [])) > 0:
                    if word.lower() == sub_dict.get('alternatives')[0].get("content"):
                        word_time_info = words_info.get(word)
                        word_time_info.append(
                            {"speech_start_time": float(sub_dict.get("start_time")), "speech_end_time": float(sub_dict.get("end_time"))})
                        words_info[word] = word_time_info
        return words_info

from model.response_emotion_extration.Interface.IResponseEmotionExtraction import IResponseTextExtraction


class AWSStrategy(IResponseTextExtraction):

    def __init__(self):
        pass

    def extract_emotion_by_time(self, response: list, time: int, negative_gap: int = 0, positive_gap: int = 0,
                                step_size: int = 500, verbose: bool = False) -> (str, int):
        """
        Questa funzione permette di estrarre le emozioni da una risposta del servizio AWS, piu vicino possibile ad un istante dato.
        :param response: Lista di emozioni
        :param time: Tempo (in ms) dal quale estrarre l'emozione
        :param negative_gap: Delta nel quale cercare l'emozione (precedente a time). Se < 0 il limite sinistro viene impostato a 0.
        :param positive_gap: Delta nel quale cercare l'emozione (successivo a time). Se < 0 il limite destro viene impostato all'ultimo istante della lista fornita.
        :param step_size: Step incrementale per la ricerca del'emozione.
        :param verbose: Flag di verbosity
        :return: Tupla contenente l'emozione e il timestamp. Se non è stata trovata alcuna emozione sarà restituito (UNKNOWN, 0)
        """
        lower_bound = time - negative_gap if negative_gap >= 0 else 0
        upper_bound = time + positive_gap if positive_gap >= 0 else response[-1].get("Timestamp", 99999999999999)
        instant_to_check = list(range(lower_bound, upper_bound + 1, step_size))
        if verbose:
            start_example = instant_to_check[0:3]
            example = [str(e) for e in start_example]
            end_example = instant_to_check[-1]
            print(f"Time To Search Is {time}, I Will Search In Range [{lower_bound}, {upper_bound}] With Step"
                  f" {step_size}. E.g. {', '.join(example)}...{str(end_example)}")
        possible_emotions = []
        time_differences = []
        for emotion in response:
            emotion_time = emotion.get("Timestamp", None)
            if emotion_time in instant_to_check:
                possible_emotions.append(emotion)
                time_differences.append(abs(time - emotion_time))
        try:
            min_difference = min(time_differences)
            min_difference_idx = time_differences.index(min_difference)
            emotion = possible_emotions[min_difference_idx]
            timestamp = int(emotion.get("Timestamp"))
            if verbose:
                print(f"Given Time Is {time}ms. Nearest Time {timestamp}ms With {min_difference}ms Of Discrepancy")

            emotions_probs_list = emotion.get("Face", {}).get("Emotions", [])
            prob_emotions = []
            possible_emotions = []
            for emotion in emotions_probs_list:
                possible_emotions.append(emotion.get("Type"))
                prob_emotions.append(emotion.get("Confidence"))
            possible_emotion_idx = prob_emotions.index(max(prob_emotions))
            result = possible_emotions[possible_emotion_idx]
        except:
            result = "UNKNOWN"
            timestamp = 0
        return result, timestamp

import json
from model.response_text_extraction.factory.ResponseTextExtractionFactory import ResponseTextExtractionFactory
from model.response_emotion_extration.factory.ResponseEmotionExtractionFactory import ResponseEmotionExtractionFactory
from keybert import KeyBERT
import spacy


def read_file(file_path: str) -> dict:
    """
    Questa funzione permette di leggere un file json
    :param file_path: Path del file da leggere
    :return : Dizionario rappresentante il file json
    """
    if not file_path.endswith(".json"):
        file_path += ".json"
    with open(file_path) as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
    return data


def print_results(data: dict) -> None:
    """
    Questa funzione permette un pretty print dei risultati ottenuti
    :param data: Dizionario dei risultati che ha come chiave, le parole trovate, e come valori dei dizionari con informazioni relative a tempi ed emozioni
    :return: None
    """
    print("Le 5 parole contestualmente piu' usate e le rispettive emozioni sono:")
    for idx, word in enumerate(data.keys()):
        res_list = data.get(word)
        print(f"{idx}. {word}:")
        for info in res_list:
            print(f"      Al Tempo {info.get('speech_start_time')} con Emozione {info.get('emotion')}")


def main():
    # Ho scelto spacy, in quanto già utilizzato in passato per il preprocessing del testo, per recuperare le stopwords
    # della lingua italiana da passare al transformer. NB per l'installazione lanciare da terminale il comando
    # python3 -m spacy download it_core_news_sm
    it = spacy.load('it_core_news_sm')
    stopwords = list(it.Defaults.stop_words)

    # Lettura dei file JSON
    transcription_dict = read_file("transcription")
    emotion_list = list(read_file("rekognition"))

    # Per mancanza di tempo si è omesso il diagramma UML, in riferimento a queste due classi sottostanti,
    # si è optato come scelta progettuale, per l'utilizzo di una Factory singleton alla quale è stata demandata
    # la responsabilità di creazione degli oggetti per l'estrazione di emozioni e testo.
    # Per queste due ultime classi si è scelto il design pattern Strategy in modo da poter consentire
    # la compatibilità anche con altri servizi (aggiungendo apposite classi) minimizzando l'impatto nel codice esistente.
    text_extractor = ResponseTextExtractionFactory().get_text_extraction_object()
    emotion_extractor = ResponseEmotionExtractionFactory().get_emotion_extraction_object()
    text = text_extractor.extract_text(transcription_dict).lower()

    # Ho scelto questo modelli in particolare (tra quelli disponibili in huggingFace di tipo FillMask)
    # è stato quello che a parere mio ha restituito risultati più pertinenti.
    # I risultati sono riportati commentati sopra ogni modello utilizzato
    # ['motivatore', 'paura', 'migliorano', 'condivisione', 'lavorare']
    model_name = "dbmdz/bert-base-italian-xxl-cased"

    # ['compito', 'piace', 'lavorare', 'idee', 'aiuta']
    # model_name = "dbmdz/bert-base-italian-cased"

    # ['migliorano', 'dimenticarsi', 'riesco', 'lavorare', 'difficoltà']
    # model_name = "dbmdz/bert-base-italian-xxl-uncased"

    # ['motivatore', 'lavoretti', 'progetto', 'assumermi', 'infine']
    # model_name = "dbmdz/bert-base-italian-uncased"

    kw_model = KeyBERT(model=model_name)
    # Qui si è giocato un poco con gli iperparametri e alla fine si sono scelti quelli riportati.
    # Si è scelto un livello di diversità basso perchè aumentandolo si ottenevano risultati fuori contesto.
    # maxsum --> permette di diversificare i risultati.
    # use_mmr=True, diversity=0.1 --> permettono la diversificazione, uso una bassa diversificazione
    # NB con keyphrase_ngram_range=(1, x > 1) non vengono trovate le parole nella trascrizione.
    data = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=stopwords,
                                     use_maxsum=False, top_n=5, use_mmr=True, diversity=0.1)
    time_info = text_extractor.extract_time_from_transcription(data, transcription_dict)
    for word in time_info.keys():
        times = time_info.get(word)
        for time_dict in times:
            time_to_search = int(time_dict.get("speech_start_time") * 1000)
            emotion, timestamp = emotion_extractor.extract_emotion_by_time(emotion_list, time_to_search,
                                                                           negative_gap=-1, positive_gap=-1,
                                                                           step_size=1, verbose=True)
            time_dict.update({"emotion": emotion, "emotion_time": timestamp})

    print(time_info)
    print_results(time_info)


if __name__ == "__main__":
    main()

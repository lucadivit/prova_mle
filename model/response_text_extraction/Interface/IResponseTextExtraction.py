import abc


class IResponseTextExtraction(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'extract_text') and callable(subclass.extract_text) \
               and hasattr(subclass, 'extract_time_from_transcription') and callable(subclass.extract_time_from_transcription) \
               or NotImplemented

    @abc.abstractmethod
    def extract_text(self, data: dict) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def extract_time_from_transcription(self, words_list: list, data: dict) -> dict:
        raise NotImplementedError

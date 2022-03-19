import abc


class IResponseTextExtraction(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'extract_emotion_by_time') and callable(subclass.extract_emotion_by_time) \
               or NotImplemented

    @abc.abstractmethod
    def extract_emotion_by_time(self, response: list, time: int, negative_gap: int = 0, positive_gap: int = 0,
                                step_size: int = 500, verbose: bool = False) -> (str, int):
        raise NotImplementedError

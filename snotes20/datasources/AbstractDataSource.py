from abc import ABCMeta, abstractmethod

class AbstractDataSource:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def get_podcasts(cls):
        pass

    @classmethod
    @abstractmethod
    def get_episodes(cls, date_start, date_end):
        pass

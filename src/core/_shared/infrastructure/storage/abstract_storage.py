from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def store(self, file_path: str, content: bytes, content_type: str):
        raise NotImplementedError
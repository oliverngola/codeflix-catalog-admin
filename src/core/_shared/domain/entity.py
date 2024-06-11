from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import uuid

from src.core._shared.domain.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification, init=False)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    @abstractmethod
    def validate(self):
        pass
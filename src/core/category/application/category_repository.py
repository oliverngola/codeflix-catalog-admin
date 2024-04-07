from abc import ABC, abstractmethod

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id) -> Category:
        raise NotImplementedError

    @abstractmethod
    def save(self, category):
        raise NotImplementedError


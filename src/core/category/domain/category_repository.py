from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, id) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[Category]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError


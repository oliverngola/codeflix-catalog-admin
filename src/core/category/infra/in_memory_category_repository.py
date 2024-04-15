from uuid import UUID
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category

class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []

    def get_by_id(self, id: UUID) -> Category | None:
        for category in self.categories:
            if category.id == id:
                return category
        return None

    def save(self, category) -> None:  
        self.categories.append(category)

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        self.categories.remove(category)
        return None
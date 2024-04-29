from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
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
        if category:
            self.categories.remove(category)

    def list(self) -> list[Category]:
        return [category for category in self.categories]

    def update(self, category: Category) -> None:
        old_category = self.get_by_id(id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)

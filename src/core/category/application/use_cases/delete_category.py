from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound

class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    
    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        category = self.repository.get_by_id(id=input.id)
        if category is None:
            raise CategoryNotFound(f"Category with {input.id} not found")
        self.repository.delete(id=category.id)

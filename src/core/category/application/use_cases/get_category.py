from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound


class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        description: str
        is_active: bool

    def execute(self, input: Input) -> Output:
        category = self.repository.get_by_id(id=input.id)
        if category is None:
            raise CategoryNotFound(f"Category with {input.id} not found")
        return self.Output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
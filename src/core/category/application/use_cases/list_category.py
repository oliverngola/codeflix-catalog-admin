from dataclasses import dataclass
from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool

class ListCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[CategoryOutput]

    def execute(self, input: Input) -> Output:
        categories = self.repository.list()

        return self.Output(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ]
        )
from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import InvalidCategory
from src.core.category.domain.category import Category



class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        name: str
        description: str = ""
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            category = Category(
                name=input.name, 
                description=input.description, 
                is_active=input.is_active
            )
        except ValueError as err:
            raise InvalidCategory(err)
        self.repository.save(category)
        return self.Output(id=category.id)

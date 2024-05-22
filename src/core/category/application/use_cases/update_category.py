from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategory


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        description: str | None = None
        is_active: bool | None = None

    def execute(self, input: Input) -> None:
        category = self.repository.get_by_id(id=input.id)
        if category is None:
            raise CategoryNotFound(f"Category with {input.id} not found")

        try:
            if input.is_active is True:
                category.activate()

            if input.is_active is False:
                category.deactivate()

            current_name = input.name if input.name is not None else category.name
            current_description =  input.description if input.description is not None else category.description
            category.update_category(name=current_name, description=current_description)
        except ValueError as error:
            raise InvalidCategory(error)

        self.repository.update(category)
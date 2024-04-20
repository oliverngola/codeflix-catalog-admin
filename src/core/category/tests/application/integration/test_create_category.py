from uuid import UUID
import pytest

from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.exceptions import InvalidCategory
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        
        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        
        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "Filmes"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active is True

    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategory, match="name cannot be empty") as exc_info:
            use_case = CreateCategory(repository=InMemoryCategoryRepository())
            response = use_case.execute(CreateCategoryRequest(name=""))

        assert exc_info.type is InvalidCategory
        assert str(exc_info.value) == "name cannot be empty"

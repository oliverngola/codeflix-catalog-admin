from uuid import UUID
import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_category_get_by_id(self):
        category_filme = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name="Serie",
            description="Categoria para serie",
            is_active=True
        )

        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_filme.id)
        
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_filme.id,
            name=category_filme.name,
            description=category_filme.description,
            is_active=category_filme.is_active
        )

    def test_when_category_does_not_exit_then_raise_exception(self):
        category_filme = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name="Serie",
            description="Categoria para serie",
            is_active=True
        )

        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])
        use_case = GetCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)


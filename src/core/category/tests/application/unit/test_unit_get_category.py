from unittest.mock import create_autospec
import pytest, uuid

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category


class TestUnitGetCategory:
    def test_category_get_by_id(self):
        category = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = category
        use_case = GetCategory(repository=mock_respository)
        request = GetCategoryRequest(id=uuid.uuid4())
        
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def test_when_category_not_found_then_raise_exception(self):
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = None
        use_case = GetCategory(repository=mock_respository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound):        
            response = use_case.execute(request)

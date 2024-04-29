from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_respository)
        use_case.execute(DeleteCategoryRequest(id=category.id))
        
        mock_respository.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_then_raise_exception(self):
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = None

        use_case = DeleteCategory(mock_respository)

        with pytest.raises(CategoryNotFound):
            use_case.execute(DeleteCategoryRequest(id=uuid.uuid4()))
        
        mock_respository.delete.assert_not_called()
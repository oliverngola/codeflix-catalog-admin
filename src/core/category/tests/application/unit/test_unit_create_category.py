from unittest.mock import MagicMock
from uuid import UUID
import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.application.use_cases.exceptions import InvalidCategory


class TestUnitCreateCategory:
	def test_create_category_with_valid_data(self):
		mock_repository = MagicMock(CategoryRepository)
		use_case = CreateCategory(repository=mock_repository)
		request = CreateCategoryRequest(
			name="Filmes",
			description="Categoria para filmes",
			is_active=True
		)
		
		response = use_case.execute(request)

		assert response.id is not None
		assert isinstance(response, CreateCategoryResponse)
		assert isinstance(response.id, UUID)
		assert mock_repository.save.called is True

	def test_create_category_with_invalid_data(self):
		with pytest.raises(InvalidCategory, match="name cannot be empty") as exc_info:
			use_case = CreateCategory(repository=MagicMock(CategoryRepository))
			response = use_case.execute(CreateCategoryRequest(name=""))

		assert exc_info.type is InvalidCategory
		assert str(exc_info.value) == "name cannot be empty"

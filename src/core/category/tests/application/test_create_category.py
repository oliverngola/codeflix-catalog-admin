from unittest.mock import MagicMock
from uuid import UUID
import pytest

from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
	def test_create_category_with_valid_data(self):
		mock_repository = MagicMock(InMemoryCategoryRepository)
		use_case = CreateCategory(repository=mock_repository)
		request = CreateCategoryRequest(
			name="Filmes",
			description="Categoria para filmes",
			is_active=True
		)
		
		category_id = use_case.execute(request)

		assert category_id is not None
		assert isinstance(category_id, UUID)
		assert mock_repository.save.called is True

	def test_create_category_with_invalid_data(self):
		with pytest.raises(InvalidCategoryData, match="name cannot be empty") as exc_info:
			use_case = CreateCategory(repository=MagicMock(InMemoryCategoryRepository))
			category_id = use_case.execute(CreateCategoryRequest(name=""))

		assert exc_info.type is InvalidCategoryData
		assert str(exc_info.value) == "name cannot be empty"
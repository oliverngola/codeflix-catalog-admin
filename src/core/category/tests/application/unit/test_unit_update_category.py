from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_respository)
        input = UpdateCategory.Input(
            id=category.id,
            name="Series"
        )
        
        use_case.execute(input)

        assert category.name == "Series"
        assert category.description == "Categoria para filmes"
        mock_respository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_respository)
        input = UpdateCategory.Input(
            id=category.id,
            description="Categoria para séries"
        )
        
        use_case.execute(input)

        assert category.name == "Filmes"
        assert category.description == "Categoria para séries"
        mock_respository.update.assert_called_once_with(category)

    def test_activate_category(self):
        category = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=False
        )
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_respository)
        input = UpdateCategory.Input(
            id=category.id,
            is_active=True
        )
        
        use_case.execute(input)

        assert category.is_active is True
        mock_respository.update.assert_called_once_with(category)
    
    def test_deactivate_category(self):
        category = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        mock_respository = create_autospec(CategoryRepository)
        mock_respository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_respository)
        input = UpdateCategory.Input(
            id=category.id,
            is_active=False
        )
        use_case.execute(input)

        assert category.is_active is False
        assert category.name == "Filmes"
        assert category.description == "Categoria para filmes"
        mock_respository.update.assert_called_once_with(category)


from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, 
    documentary_category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

class TestUpdateGenre:
    def test_update_genre_without_categories(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories,
    ):
        genre = Genre(name="Action")
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository_with_categories)

        request = UpdateGenre.Input(
            id=genre.id,
            name="Romance",
            categories=set({}),
            is_active=False,
        )
        use_case.execute(request)

        assert genre.name == "Romance"
        assert genre.categories == set({})
        mock_genre_repository.update.assert_called_once_with(genre)

    def test_update_genre_with_categories(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories,
        movie_category,
        documentary_category
    ):
        genre = Genre(name="Action")
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository_with_categories)

        request = UpdateGenre.Input(
            id=genre.id,
            name="Romance",
            categories={movie_category.id, documentary_category.id},
            is_active=False,
        )
        use_case.execute(request)

        assert genre.name == "Romance"
        assert genre.categories == {movie_category.id, documentary_category.id}
        mock_genre_repository.update.assert_called_once_with(genre)

    def test_update_genre_raise_exception_when_categories_are_invalid(
        self,
        mock_genre_repository,
        mock_category_repository_with_categories
    ):
        genre = Genre(name="Action")
        mock_genre_repository.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository_with_categories)
        
        cat_id = uuid.uuid4()
        request = UpdateGenre.Input(
            id=genre.id,
            name="Romance",
            categories={cat_id},
            is_active=False,
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(request)

        assert str(cat_id) in str(exc_info.value)

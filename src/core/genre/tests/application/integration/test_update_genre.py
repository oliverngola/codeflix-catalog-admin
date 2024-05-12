import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[
            movie_category,
            documentary_category
        ]
    )

@pytest.fixture
def empty_category_repository() -> CategoryRepository:
    return InMemoryCategoryRepository()

class TestUpdateGenre:
    def test_update_genre_without_categories(
        self,
        empty_category_repository,
    ):
        genre = Genre(name="Action")
        repository = InMemoryGenreRepository()
        repository.save(genre=genre)
        use_case = UpdateGenre(repository=repository, category_repository=empty_category_repository)

        request = UpdateGenre.Input(
            id=genre.id,
            name="Romance",
            categories=set({}),
            is_active=False,
        )
        output = use_case.execute(request)

        updated_genre = repository.get_by_id(genre.id)
        assert output is None
        assert updated_genre.name == "Romance"
        assert updated_genre.is_active is False

    def test_update_genre_with_categories(
        self,
        category_repository,
        movie_category,
        documentary_category
    ):
        genre = Genre(name="Action")
        repository = InMemoryGenreRepository()
        repository.save(genre=genre)
        use_case = UpdateGenre(repository=repository, category_repository=category_repository)

        request = UpdateGenre.Input(
            id=genre.id,
            name="Romance",
            categories={movie_category.id, documentary_category.id},
            is_active=False,
        )
        output = use_case.execute(request)

        updated_genre = repository.get_by_id(genre.id)
        assert output is None
        assert updated_genre.name == "Romance"
        assert updated_genre.is_active is False
        assert updated_genre.categories == {movie_category.id, documentary_category.id }

    def test_update_genre_raise_exception_when_categories_are_invalid(
        self,
        category_repository,
    ):
        genre = Genre(name="Action")
        repository = InMemoryGenreRepository()
        repository.save(genre=genre)
        use_case = UpdateGenre(repository=repository, category_repository=category_repository)
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
    
    
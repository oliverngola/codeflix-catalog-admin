import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound
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

class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        category_repository,
        movie_category,
        documentary_category
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(genre_repository, category_repository)

        input = CreateGenre.Input(
            name="Romance",
            category_ids={movie_category.id, documentary_category.id},
        )

        output = use_case.execute(input)
        assert output.id is not None
        assert isinstance(output, CreateGenre.Output)
        assert isinstance(output.id, uuid.UUID)
        saved_genere = genre_repository.get_by_id(output.id)
        assert saved_genere is not None
        assert saved_genere.name == "Romance"
        assert saved_genere.categories == {movie_category.id, documentary_category.id }
        assert saved_genere.is_active is True

    def test_create_genre_without_categories(
        self,
        empty_category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(genre_repository, empty_category_repository)

        input = CreateGenre.Input(
            name="Action"
        )

        output = use_case.execute(input)
        assert output.id is not None
        assert isinstance(output, CreateGenre.Output)
        assert isinstance(output.id, uuid.UUID)
        saved_genere = genre_repository.get_by_id(output.id)
        assert saved_genere is not None
        assert saved_genere.name == "Action"
        assert saved_genere.categories == set({})
        assert saved_genere.is_active is True

    def test_create_genre_with_inexistent_categories_raise_an_error(
        self,
        empty_category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(genre_repository, empty_category_repository)

        category_id1 = uuid.uuid4()
        category_id2 = uuid.uuid4()
        input = CreateGenre.Input(
            name="Romance",
            category_ids={category_id1, category_id2},
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)

        assert exc_info.type is RelatedCategoriesNotFound
        assert str(category_id1) in str(exc_info.value)
        assert str(category_id2) in str(exc_info.value)


import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
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

class TestListGenre:
    def test_list_genres_with_associated_category(
        self,
        category_repository,
        movie_category,
        documentary_category
    ):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name="Drama",
            categories={movie_category.id, documentary_category.id},
        )
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=True,
                    categories={movie_category.id, documentary_category.id}
                )
            ]
        )
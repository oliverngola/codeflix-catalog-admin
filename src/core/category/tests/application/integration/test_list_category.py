import pytest
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListOutputMeta
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    @pytest.fixture
    def category_movie(self) -> Category:
        return Category(
            name="Filme",
            description="Categoria de filmes",
        )

    @pytest.fixture
    def category_series(self) -> Category:
        return Category(
            name="Séries",
            description="Categoria de séries",
        )

    def test_when_no_categories_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=empty_repository)
        output = use_case.execute(input=ListCategory.Input())

        assert output == ListCategory.Output(data=[])

    def test_when_categories_exist_then_return_mapped_list(
        self,
        category_movie: Category,
        category_series: Category,
    ) -> None:
        repository = InMemoryCategoryRepository()
        repository.save(category=category_movie)
        repository.save(category=category_series)

        use_case = ListCategory(repository=repository)
        output = use_case.execute(input=ListCategory.Input())

        assert output == ListCategory.Output(
            data=[
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                ),
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2,
            ),
        )
import uuid, pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.delete_category  import DeleteCategory
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_filme = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name="Serie",
            description="Categoria para serie",
            is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])

        use_case = DeleteCategory(repository=repository)
        input = DeleteCategory.Input(id=category_filme.id)
        
        assert repository.get_by_id(category_filme.id) is not None
        output = use_case.execute(input)
               
        assert repository.get_by_id(category_filme.id) is None
        assert output is None
        assert len(repository.categories) == 1


    def test_when_category_does_not_exit_then_raise_exception(self):
        category_filme = Category(
            name="Filmes",
            description="Categoria para filmes",
            is_active=True
        )
        category_serie = Category(
            name="Serie",
            description="Categoria para serie",
            is_active=True
        )

        repository = InMemoryCategoryRepository(categories=[category_filme, category_serie])
        use_case = DeleteCategory(repository=repository)
        not_found_id = uuid.uuid4()
        input = DeleteCategory.Input(id=not_found_id)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(input)


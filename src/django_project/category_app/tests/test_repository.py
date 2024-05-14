import uuid
import pytest
from core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_category_in_database(self):    
        category = Category(
            name="Movie",
            description="Movie Category",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get()
        assert category_db.id == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active


@pytest.mark.django_db
class TestGetById:
    def test_can_get_category_by_id(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category_filme)
        repository.save(category_serie)

        category = repository.get_by_id(category_filme.id)

        assert category.id == category_filme.id
        assert category.name == category_filme.name
        assert category.description == category_filme.description
        assert category.is_active == category.is_active

    def test_when_category_does_not_exists_should_return_none(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category_filme)

        category = repository.get_by_id(uuid.uuid4())

        assert CategoryModel.objects.count() == 1
        assert category is None


@pytest.mark.django_db
class TestDelete:
    def test_delete_category(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category_filme)
        repository.save(category_serie)

        assert CategoryModel.objects.count() == 2
        repository.delete(category_filme.id)

        assert CategoryModel.objects.count() == 1


@pytest.mark.django_db
class TestList:
    def test_list_categories(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category_filme)
        repository.save(category_serie)

        category = repository.list()

        assert CategoryModel.objects.count() == 2
        assert len(category) == 2

    def test_list_empty_categories(self):
        repository = DjangoORMCategoryRepository(CategoryModel)

        category = repository.list()

        assert CategoryModel.objects.count() == 0
        assert len(category) == 0


@pytest.mark.django_db
class TestUpdate:
    def test_update_category(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category_filme)
        repository.save(category_serie)

        category_filme.name = "Filmes"
        category_filme.description = "Categoria para filmes e séries"
        repository.update(category_filme)

        assert CategoryModel.objects.count() == 2
        updated_category = repository.get_by_id(category_filme.id)
        assert updated_category.name == "Filmes"
        assert updated_category.description == "Categoria para filmes e séries"

    def test_update_non_existent_category_does_not_raise_exception(self):
        repository = DjangoORMCategoryRepository(CategoryModel)

        category = Category(
            name="Documentário",
            description="Categoria para documentários",
        )
        repository.update(category)

        assert CategoryModel.objects.count() == 0


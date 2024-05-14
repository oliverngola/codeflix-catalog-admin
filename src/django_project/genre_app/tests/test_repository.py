import uuid
import pytest
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.models import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
class TestSave:
    def test_saves_genre(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == "Action"
        assert genre_model.is_active is True

    def test_saves_genre_with_categories(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre = Genre(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )

        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.get(id=genre.id)
        related_category = genre_model.categories.all()
        assert related_category[0].id in {movie_category.id, documentary_category.id}
        assert related_category[1].id in {movie_category.id, documentary_category.id}


@pytest.mark.django_db
class TestGetById:
    def test_can_get_genre_by_id(self):
        genre = Genre(name="Action")
        repository = DjangoORMGenreRepository()
        repository.save(genre)

        saved_genre = repository.get_by_id(id=genre.id)
        assert saved_genre.id == genre.id
        assert saved_genre.name == genre.name
        assert saved_genre.categories == set({})

    def test_when_genre_does_not_exists_should_return_none(self):
        repository = DjangoORMGenreRepository()

        saved_genre = repository.get_by_id(id=uuid.uuid4())
        assert saved_genre is None
        

@pytest.mark.django_db
class TestDelete:
    def test_delete_genre(self):
        genre_action = Genre(name="Action")
        genre_romance = Genre(name="Romance")
        repository = DjangoORMGenreRepository()
        repository.save(genre_action)
        repository.save(genre_romance)

        assert GenreORM.objects.count() == 2
        repository.delete(genre_action.id)

        assert GenreORM.objects.count() == 1


@pytest.mark.django_db
class TestList:
    def test_list_genres(self):
        genre_action = Genre(name="Action")
        genre_romance = Genre(name="Romance")
        repository = DjangoORMGenreRepository()
        repository.save(genre_action)
        repository.save(genre_romance)

        genre = repository.list()

        assert GenreORM.objects.count() == 2
        assert len(genre) == 2

    def test_list_empty_genres(self):
        repository = DjangoORMGenreRepository()

        genre = repository.list()

        assert GenreORM.objects.count() == 0
        assert len(genre) == 0


@pytest.mark.django_db
class TestUpdate:
    def test_update_genre(self):
        genre_action = Genre(name="Action")
        genre_romance = Genre(name="Romance")
        repository = DjangoORMGenreRepository()
        repository.save(genre_action)
        repository.save(genre_romance)
        
        genre_action.name = "Action Plus"
        repository.update(genre_action)

        assert GenreORM.objects.count() == 2
        updated_genre = repository.get_by_id(genre_action.id)
        assert updated_genre.name == "Action Plus"

    def test_update_non_existent_genre_does_not_raise_exception(self):
        repository = DjangoORMGenreRepository()

        genre = Genre(name="Action")
        repository.update(genre)

        assert GenreORM.objects.count() == 0



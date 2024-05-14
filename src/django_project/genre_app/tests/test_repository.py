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
        assert related_category[0].id == movie_category.id
        assert related_category[1].id == documentary_category.id

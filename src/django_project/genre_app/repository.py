from uuid import UUID
from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM

class DjangoORMGenreRepository(GenreRepository):
    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = GenreORM.objects.get(id=id)
            return GenreModelMapper.to_entity(genre_model)
        except GenreORM.DoesNotExist:
            return None

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_orm = GenreModelMapper.to_model(genre)
            genre_orm.save()
            genre_orm.categories.set(genre.categories)
    
    def delete(self, id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()
    
    def list(self) -> list[Genre]:
        return [
            GenreModelMapper.to_entity(genre_model)
            for genre_model in GenreORM.objects.all()
        ]
    
    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return None
        
        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)

class GenreModelMapper:
    @staticmethod
    def to_entity(model: GenreORM) -> Genre:
        return Genre(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            categories={category.id for category in model.categories.all()},
        )

    @staticmethod
    def to_model(entity: Genre) -> GenreORM:
        return GenreORM(
            id=entity.id,
            name=entity.name,
            is_active=entity.is_active,
        )
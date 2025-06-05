import uuid
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestSave:
    def test_can_save_genre(self):
        repository = InMemoryGenreRepository()
        genre = Genre(
            name="Ação"
        )

        repository.save(genre)

        assert len(repository.genres) == 1
        assert repository.genres[0] == genre

    def test_can_save_genre_with_id(self):
        repository = InMemoryGenreRepository()
        genre = Genre(
            id=uuid.uuid4(),
            name="Ação",
            is_active=False,
        )

        repository.save(genre)

        assert len(repository.genres) == 1
        assert repository.genres[0] == genre

    def test_can_save_multiple_genres(self):
        repository = InMemoryGenreRepository()
        genre1 = Genre(
            name="Ação"
        )
        genre2 = Genre(
            name="Comédia"
        )

        repository.save(genre1)
        repository.save(genre2)

        assert len(repository.genres) == 2
        assert repository.genres[0] == genre1
        assert repository.genres[1] == genre2

    def test_can_save_genre_with_category(self):
        repository = InMemoryGenreRepository()
        genre = Genre(
            name="Ação",
            categories=[uuid.uuid4(), uuid.uuid4()]
        )

        repository.save(genre)

        assert len(repository.genres) == 1
        assert repository.genres[0] == genre

class TestGetById:
    def test_can_get_genre_by_id(self):
        genre_action = Genre(
            name="Ação",
        )
        genre_comedy = Genre(
            name="Comédia",
        )
        repository = InMemoryGenreRepository(
            genres=[
                genre_action,
                genre_comedy,
            ]
        )

        genre = repository.get_by_id(genre_action.id)

        assert genre == genre_action

    def test_when_genre_does_not_exists_should_return_none(self):
        genre_action = Genre(
            name="Ação",
        )
        repository = InMemoryGenreRepository(
            genres=[
                genre_action,
            ]
        )

        genre = repository.get_by_id(uuid.uuid4())

        assert genre is None

class TestDelete:
    def test_delete_genre(self):
        genre_action = Genre(
            name="Ação",
        )
        genre_comedy = Genre(
            name="Comédia",
        )
        repository = InMemoryGenreRepository(
            genres=[
                genre_action,
                genre_comedy,
            ]
        )

        repository.delete(genre_action.id)

        assert len(repository.genres) == 1
        assert repository.genres[0] == genre_comedy

    def test_delete_non_existent_genre(self):
        genre_action = Genre(
            name="Ação",
        )
        repository = InMemoryGenreRepository(
            genres=[
                genre_action,
            ]
        )

        repository.delete(uuid.uuid4())

        assert len(repository.genres) == 1
        assert repository.genres[0] == genre_action

class TestList:
    def test_list_genres(self):
        genre_action = Genre(
            name="Ação",
        )
        genre_comedy = Genre(
            name="Comédia",
        )
        repository = InMemoryGenreRepository(
            genres=[
                genre_action,
                genre_comedy,
            ]
        )

        genres = repository.list()

        assert len(genres) == 2
        assert genres[0] == genre_action
        assert genres[1] == genre_comedy

    def test_list_empty_genres(self):
        repository = InMemoryGenreRepository()

        genres = repository.list()

        assert len(genres) == 0

class TestUpdate:
    def test_update_genre(self):
        genre_action = Genre(
            name="Ação",
        )
        repository = InMemoryGenreRepository(
            genres=[
                genre_action,
            ]
        )

        genre_action.change_name("Ação Atualizada")
        repository.update(genre_action)

        assert len(repository.genres) == 1
        assert repository.genres[0].name == "Ação Atualizada"

    def test_update_non_existent_genre(self):
        genre_action = Genre(
            name="Ação",
        )
        repository = InMemoryGenreRepository()

        try:
            repository.update(genre_action)
        except ValueError as e:
            assert str(e) == "Genre not found"
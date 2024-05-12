import uuid, pytest

from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre  import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        genre_action = Genre(name="Action")
        genre_romance = Genre(name="Romance")
        repository = InMemoryGenreRepository(genres=[genre_action, genre_romance])

        use_case = DeleteGenre(repository=repository)
        input = DeleteGenre.Input(id=genre_action.id)
        
        assert repository.get_by_id(genre_action.id) is not None
        output = use_case.execute(input)
               
        assert repository.get_by_id(genre_action.id) is None
        assert output is None
        assert len(repository.genres) == 1


    def test_when_genre_does_not_exit_then_raise_exception(self):
        genre_action = Genre(name="Action")
        genre_romance = Genre(name="Romance")

        repository = InMemoryGenreRepository(genres=[genre_action, genre_romance])
        use_case = DeleteGenre(repository=repository)
        not_found_id = uuid.uuid4()
        input = DeleteGenre.Input(id=not_found_id)

        with pytest.raises(GenreNotFound, match="Genre with .* not found") as exc:
            use_case.execute(input)


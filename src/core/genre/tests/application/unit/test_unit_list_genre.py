from unittest.mock import create_autospec
import uuid

from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository

class TestListGenre:
    def test_list_genres_with_associated_category(self):
        mock_genre_repository = create_autospec(GenreRepository)

        cat_id1 = uuid.uuid4()
        cat_id2 = uuid.uuid4()

        drama_genre = Genre(
            name="Drama",
            categories={cat_id1, cat_id2}
        )
        action_genre = Genre(name="Action",)
        mock_genre_repository.list.return_value = [drama_genre, action_genre]

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=drama_genre.id,
                    name="Drama",
                    categories={cat_id1, cat_id2},
                    is_active=True,
                ), 
                GenreOutput(
                    id=action_genre.id,
                    name="Action",
                    categories=set({}),
                    is_active=True,
                )
            ]
        )

    def test_list_of_empty_genres(self):
        mock_genre_repository = create_autospec(GenreRepository)
        mock_genre_repository.list.return_value = []

        use_case = ListGenre(repository=mock_genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert output == ListGenre.Output(
            data=[]
        )

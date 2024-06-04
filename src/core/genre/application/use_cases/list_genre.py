from dataclasses import dataclass
from uuid import UUID

from src import config
from src.core._shared.application.list import ListOutput, ListOutputMeta
from src.core.genre.domain.genre_repository import GenreRepository

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1

    @dataclass
    class Output(ListOutput[GenreOutput]):
        pass

    def execute(self, input: Input) -> Output:
        genres = self.repository.list()
        ordered_genres = sorted(
            genres,
            key=lambda genre: getattr(genre, input.order_by),
        )
        page_offset = (input.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        genres_page = ordered_genres[page_offset:page_offset + config.DEFAULT_PAGINATION_SIZE]

        return self.Output(
            data=sorted(
                [
                    GenreOutput(
                        id=genre.id,
                        name=genre.name,
                        is_active=genre.is_active,
                        categories=genre.categories,
                    )
                    for genre in genres_page
                ],
                key=lambda genre: getattr(genre, input.order_by),
            ),
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(genres),
            ),
        )

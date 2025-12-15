from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.domain.video_repository import VideoRepository
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.genre.domain.genre_repository import GenreRepository



class GetVideo:
    def __init__(self, 
        repository: VideoRepository,
        category_repository: CategoryRepository,
        cast_member_repository: CastMemberRepository,
        genre_repository: GenreRepository
    ) -> None:
        self.repository = repository
        self.category_repository = category_repository
        self.cast_member_repository = cast_member_repository
        self.genre_repository = genre_repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        title: str
        description: str
        year_launched: int
        opened: bool
        duration: Decimal
        link: str
        categories: list[str]
        cast_members: list[str]
        genres: list[str]
        thumb_file_url: str
        banner_file_url: str
        video_file_url: str 
        rating: str

    def execute(self, input: Input) -> Output:
        video = self.repository.get_by_id(id=input.id)
        if not video:
            raise VideoNotFound(f"Video with id {input.id} not found")
        return self.Output(
            id=video.id,
            title=video.title,
            description=video.description,
            year_launched=video.launch_year,
            opened=video.opened,
            duration=video.duration,
            rating=video.rating,
            link=video.video.raw_location if video.video else "",
            categories=[
                self.category_repository.get_by_id(category).id
                for category in video.categories
            ],
            cast_members=[
                self.cast_member_repository.get_by_id(cast_member).id
                for cast_member in video.cast_members
            ],
            genres=[
                self.genre_repository.get_by_id(genre).id
                for genre in video.genres
            ],
            banner_file_url=video.banner.raw_location if video.banner else "",
            thumb_file_url=video.thumbnail.raw_location if video.thumbnail else "",
            video_file_url=video.video.raw_location if video.video else ""
        )
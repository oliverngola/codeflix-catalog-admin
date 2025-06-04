from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from src import config
from src.core._shared.application.list import ListOutput, ListOutputMeta
from src.core.category.domain.category_repository import CategoryRepository
from src.core.video.domain.video_repository import VideoRepository
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.genre.domain.genre_repository import GenreRepository

@dataclass
class VideoOutput:
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

class ListVideo:
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
        order_by: str = "title"
        current_page: int = 1

    @dataclass
    class Output(ListOutput[VideoOutput]):
        pass

    def execute(self, input: Input) -> Output:
        videos = self.repository.list()
        ordered_videos = sorted(
            videos,
            key=lambda video: getattr(video, input.order_by),
        )
        page_offset = (input.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        videos_page = ordered_videos[page_offset:page_offset + config.DEFAULT_PAGINATION_SIZE]

        return self.Output(
            data=sorted(
                [
                    VideoOutput(
                        id=video.id,
                        title=video.title,
                        description=video.description,
                        year_launched=video.launch_year,
                        opened=video.opened,
                        duration=video.duration,
                        rating=video.rating,
                        link=video.video.raw_location if video.video else "",
                        categories=[
                            self.category_repository.get_by_id(category).name
                            for category in video.categories
                        ],
                        cast_members=[
                            self.cast_member_repository.get_by_id(cast_member).name
                            for cast_member in video.cast_members
                        ],
                        genres=[
                            self.genre_repository.get_by_id(genre).name
                            for genre in video.genres
                        ],
                        banner_file_url=video.banner.raw_location if video.banner else "",
                        thumb_file_url=video.thumbnail.raw_location if video.thumbnail else "",
                        video_file_url=video.video.raw_location if video.video else "",
                    )
                    for video in videos_page
                ],
                key=lambda category: getattr(category, input.order_by),
            ),
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(videos),
            ),
        )
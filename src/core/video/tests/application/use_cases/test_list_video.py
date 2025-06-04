import pytest
from unittest.mock import create_autospec

from src.core._shared.application.list import ListOutputMeta
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.use_cases.list_video import (
    VideoOutput,
    ListVideo
)
from src.core.video.domain.video import Video


class TestListVideo:
    @pytest.fixture
    def video_one(self) -> Video:
        return Video(
            title="AAA Video",
            description="A test video",
            launch_year=2021,
            opened=True,
            duration=120,
            rating="L",
            cast_members=set(),
            categories=set(),
            genres=set(),
        )

    @pytest.fixture
    def video_second(self) -> Video:
        return Video(
            title="BBB Video",
            description="Another test video",
            launch_year=2022,
            opened=False,
            duration=90,
            rating="10",
            cast_members=set(),
            categories=set(),
            genres=set(),
        )

    @pytest.fixture
    def mock_empty_repository(self) -> VideoRepository:
        repository = create_autospec(VideoRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        video_one: Video,
        video_second: Video,
    ) -> VideoRepository:
        repository = create_autospec(VideoRepository)
        repository.list.return_value = [
            video_one,
            video_second,
        ]
        return repository
    
    def test_when_no_video_then_return_empty_list(
        self,
        mock_empty_repository: VideoRepository,
    ) -> None:
        use_case = ListVideo(
            repository=mock_empty_repository,
            category_repository=create_autospec(CategoryRepository),
            cast_member_repository=create_autospec(CastMemberRepository),
            genre_repository=create_autospec(GenreRepository),
        )
        output = use_case.execute(input=ListVideo.Input())

        assert output == ListVideo.Output(data=[])

    def test_when_video_exist_then_return_mapped_list(
        self,
        mock_populated_repository: VideoRepository,
        video_one: Video,
        video_second: Video,
    ) -> None:
        use_case = ListVideo(
            repository=mock_populated_repository,
            category_repository=create_autospec(CategoryRepository),
            cast_member_repository=create_autospec(CastMemberRepository),
            genre_repository=create_autospec(GenreRepository),
        )
        output = use_case.execute(input=ListVideo.Input())

        assert output == ListVideo.Output(
            data=[
                 VideoOutput(
                    id=video_one.id,
                    title=video_one.title,
                    description=video_one.description,
                    year_launched=video_one.launch_year,
                    opened=video_one.opened,
                    duration=video_one.duration,
                    rating=video_one.rating,
                    link="",
                    categories=[],
                    cast_members=[],
                    genres=[],
                    thumb_file_url="",
                    banner_file_url="",
                    video_file_url=""
                ),
                VideoOutput(
                    id=video_second.id,
                    title=video_second.title,
                    description=video_second.description,
                    year_launched=video_second.launch_year,
                    opened=video_second.opened,
                    duration=video_second.duration,
                    rating=video_second.rating,
                    link="",
                    categories=[],
                    cast_members=[],
                    genres=[],
                    thumb_file_url="",
                    banner_file_url="",
                    video_file_url=""
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2,
            ),
        )
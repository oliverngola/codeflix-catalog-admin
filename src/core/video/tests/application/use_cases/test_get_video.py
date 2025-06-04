from unittest.mock import create_autospec
import uuid
import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.application.use_cases.get_video import GetVideo
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video


class TestGetVideo:
    def test_get_video(self):
        video = Video(
            title="Video",
            description="A test video",
            launch_year=2021,
            opened=True,
            duration=120,
            rating="L",
            cast_members=set(),
            categories=set(),
            genres=set(),
        )

        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = video
        mock_category_repository = create_autospec(CategoryRepository)
        mock_cast_member_repository = create_autospec(CastMemberRepository)
        mock_genre_repository = create_autospec(GenreRepository)


        use_case = GetVideo(
            repository=mock_repository,
            category_repository=mock_category_repository,
            cast_member_repository=mock_cast_member_repository,
            genre_repository=mock_genre_repository,
        )
        
        response =  use_case.execute(GetVideo.Input(id=uuid.uuid4()))

        assert response == GetVideo.Output(
            id=video.id,
            title=video.title,
            description=video.description,
            year_launched=video.launch_year,
            opened=video.opened,
            duration=video.duration,
            link="",
            categories=[],
            cast_members=[],
            genres=[],
            thumb_file_url="",
            banner_file_url="",
            video_file_url="",
            rating=video.rating
        )
        mock_repository.get_by_id.assert_called_once()

    def test_video_not_found(self):
        mock_repository = create_autospec(VideoRepository)
        use_case = GetVideo(
            repository=mock_repository,
            category_repository=create_autospec(CategoryRepository),
            cast_member_repository=create_autospec(CastMemberRepository),
            genre_repository=create_autospec(GenreRepository),
        )
        mock_repository.get_by_id.return_value = None
        with pytest.raises(VideoNotFound):
            use_case.execute(GetVideo.Input(id=uuid.uuid4()))
        mock_repository.get_by_id.assert_called_once()
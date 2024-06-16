from decimal import Decimal
from pathlib import Path
from unittest.mock import create_autospec
import uuid

import pytest
from src.core._shared.infrastructure.storage.abstract_storage import AbstractStorage
from src.core.video.application.use_cases.exceptions import VideoNotFound
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestUploadVideo:
    def test_upload_video_media_to_video(self) -> None:
        video = Video(
            title="Video 1",
            description="Video 1 description",
            launch_year=2021,
            duration=Decimal(120),
            rating=Rating.AGE_14,
            opened=True,
            cast_members=set(),
            categories=set(),
            genres=set(),
        )

        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorage)
        use_case = UploadVideo(
            repository=video_repository,
            storage_service=mock_storage,
        )

        use_case.execute(
            UploadVideo.Input(
                video_id=video.id,
                file_name="video.mp4",
                content=b"video content",
                content_type="video/mp4",
            )
        )

        mock_storage.store.assert_called_once_with(
            Path(f"videos/{video.id}/video.mp4"),
            b"video content",
            "video/mp4",
        )
        assert video.video == AudioVideoMedia(
            name="video.mp4",
            raw_location=f"videos/{video.id}/video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
        )
        assert video_repository.videos[0] == video

    def test_when_video_does_not_exist_then_raise_error(self):
        video_repository = InMemoryVideoRepository(videos=[])
        mock_storage = create_autospec(AbstractStorage)
        use_case = UploadVideo(
            repository=video_repository,
            storage_service=mock_storage,
        )

        video_id = uuid.uuid4()
        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(
                UploadVideo.Input(
                    video_id=video_id,
                    file_name="video.mp4",
                    content=b"video content",
                    content_type="video/mp4",
                )
            )

        assert str(video_id) in str(exc_info.value)
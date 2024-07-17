from dataclasses import dataclass
from uuid import UUID

from src.core.video.application.use_cases.exceptions import VideoNotFound, MediaNotFound
from src.core.video.domain.value_objects import MediaType, MediaStatus
from src.core.video.domain.video_repository import VideoRepository


class ProcessAudioVideoMedia:
    @dataclass
    class Input:
        video_id: UUID
        encoded_location: str
        media_type: MediaType
        status: MediaStatus

    def __init__(self, video_repository: VideoRepository) -> None:
        self._video_repository = video_repository

    def execute(self, request: Input) -> None:
        video = self._video_repository.get_by_id(request.video_id)
        if video is None:
            raise VideoNotFound(f"Video with id {request.video_id} not found")

        if request.media_type == MediaType.VIDEO:
            if not video.video:
                raise MediaNotFound("Video must have a video media to be processed")

            video.process(status=request.status, encoded_location=request.encoded_location)

        self._video_repository.update(video)
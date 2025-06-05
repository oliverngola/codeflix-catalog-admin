import uuid

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestSave:
    def test_can_save_video(self):
        repository = InMemoryVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        assert len(repository.videos) == 1
        assert repository.videos[0] == video

    def test_can_save_video_without_media(self):
        repository = InMemoryVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories={uuid.uuid4(), uuid.uuid4()},
            genres={uuid.uuid4(), uuid.uuid4()},
            cast_members={uuid.uuid4(), uuid.uuid4()},
        )
        repository.save(video)

        assert len(repository.videos) == 1
        assert repository.videos[0] == video
        assert len(repository.videos[0].categories) == 2
        assert len(repository.videos[0].genres) == 2
        assert len(repository.videos[0].cast_members) == 2


class TestGetById:
    def test_can_get_video_by_id(self):
        repository = InMemoryVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        retrieved_video = repository.get_by_id(video.id)

        assert retrieved_video is not None
        assert retrieved_video == video

    def test_returns_none_if_video_not_found(self):
        repository = InMemoryVideoRepository()
        video = repository.get_by_id(uuid.uuid4())

        assert video is None


class TestList:
    def test_can_list_videos(self):
        repository = InMemoryVideoRepository()
        video1 = Video(
            id=uuid.uuid4(),
            title="Test Video 1",
            description="A test video 1",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video2 = Video(
            id=uuid.uuid4(),
            title="Test Video 2",
            description="A test video 2",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video1)
        repository.save(video2)

        videos = repository.list()

        assert len(videos) == 2
        assert video1 in videos
        assert video2 in videos

    def test_returns_empty_list_if_no_videos(self):
        repository = InMemoryVideoRepository()
        videos = repository.list()

        assert len(videos) == 0
        assert videos == []


class TestDelete:
    def test_can_delete_video(self):
        repository = InMemoryVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        assert len(repository.videos) == 1
        repository.delete(video.id)

        assert len(repository.videos) == 0

    def test_does_not_raise_error_when_deleting_non_existent_video(self):
        repository = InMemoryVideoRepository()
        repository.delete(uuid.uuid4())
        assert len(repository.videos) == 0


class TestUpdate:
    def test_can_update_video(self):
        repository = InMemoryVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        updated_video = Video(
            id=video.id,
            title="Updated Test Video",
            description="An updated test video",
            launch_year=2023,
            opened=False,
            duration=120,
            rating=Rating.AGE_10,
            categories={uuid.uuid4()},
            genres={uuid.uuid4()},
            cast_members={uuid.uuid4()},
        )
        repository.update(updated_video)

        retrieved_video = repository.get_by_id(video.id)
        assert retrieved_video is not None
        assert retrieved_video.title == "Updated Test Video"
        assert retrieved_video.description == "An updated test video"
        assert retrieved_video.opened is False
        assert retrieved_video.duration == 120
        assert retrieved_video.rating == Rating.AGE_10
        assert len(retrieved_video.categories) == 1
        assert len(retrieved_video.genres) == 1
        assert len(retrieved_video.cast_members) == 1

    def test_does_not_raise_error_when_updating_non_existent_video(self):
        repository = InMemoryVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Non-existent Video",
            description="This video does not exist",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.update(video)
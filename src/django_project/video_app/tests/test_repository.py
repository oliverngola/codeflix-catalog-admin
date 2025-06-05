import uuid
import pytest

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.models import Video as VideoORM
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository

@pytest.mark.django_db
class TestSave:
    def test_can_save_video(self):
        repository = DjangoORMVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        repository.save(video)

        assert VideoORM.objects.count() == 1
        video_model = VideoORM.objects.first()
        assert video_model.id == video.id
        assert video_model.title == "Test Video"
        assert video_model.description == "A test video"
        assert video_model.launch_year == 2023
        assert video_model.opened is True
        assert video_model.duration == 120
        assert video_model.rating == Rating.AGE_10
    
    def test_can_save_video_without_media(self):
        repository = DjangoORMVideoRepository()
        category_repository = DjangoORMCategoryRepository()
        genre_repository = DjangoORMGenreRepository()
        cast_member_repository = DjangoORMCastMemberRepository()
        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")
        category_repository.save(movie_category)
        category_repository.save(documentary_category)
        action_genre = Genre(name="Action")
        genre_repository.save(action_genre)
        drama_genre = Genre(name="Drama")
        genre_repository.save(drama_genre)
        actor_cast_member = CastMember(name="Actor 1", type=CastMemberType.ACTOR)
        cast_member_repository.save(actor_cast_member)
        director_cast_member = CastMember(name="Director 1", type=CastMemberType.DIRECTOR)
        cast_member_repository.save(director_cast_member)

        video = Video(
            id=uuid.uuid4(),
            title="Test Video Without Media",
            description="A test video without media",
            launch_year=2023,
            opened=True,
            duration=90,
            rating=Rating.L,
            categories={movie_category.id, documentary_category.id},
            genres={action_genre.id, drama_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )

        repository.save(video)

        assert VideoORM.objects.count() == 1
        video_model = VideoORM.objects.first()
        assert video_model.id == video.id
        assert video_model.title == "Test Video Without Media"
        assert video_model.description == "A test video without media"
        assert video_model.launch_year == 2023
        assert video_model.opened is True
        assert video_model.duration == 90
        assert video_model.rating == Rating.L
        assert video_model.categories.count() == 2
        assert video_model.genres.count() == 2
        assert video_model.cast_members.count() == 2


@pytest.mark.django_db
class TestGetById:
    def test_can_get_video_by_id(self):
        repository = DjangoORMVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        saved_video = repository.get_by_id(id=video.id)
        assert saved_video.id == video.id
        assert saved_video.title == video.title
        assert saved_video.description == video.description
        assert saved_video.launch_year == video.launch_year
        assert saved_video.opened is True
        assert saved_video.duration == video.duration
        assert saved_video.rating == video.rating

    def test_when_video_does_not_exists_should_return_none(self):
        repository = DjangoORMVideoRepository()

        saved_video = repository.get_by_id(id=uuid.uuid4())
        assert saved_video is None


@pytest.mark.django_db
class TestDelete:
    def test_delete_video(self):
        repository = DjangoORMVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        assert VideoORM.objects.count() == 1
        repository.delete(video.id)

        assert VideoORM.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_videos(self):
        repository = DjangoORMVideoRepository()
        video1 = Video(
            id=uuid.uuid4(),
            title="Test Video 1",
            description="A test video 1",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video2 = Video(
            id=uuid.uuid4(),
            title="Test Video 2",
            description="A test video 2",
            launch_year=2023,
            opened=False,
            duration=90,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video1)
        repository.save(video2)

        videos = repository.list()

        assert VideoORM.objects.count() == 2
        assert len(videos) == 2
        assert videos[0].id == video1.id or videos[1].id == video1.id
        assert videos[0].id == video2.id or videos[1].id == video2.id

    def test_list_empty_videos(self):
        repository = DjangoORMVideoRepository()

        videos = repository.list()

        assert VideoORM.objects.count() == 0
        assert len(videos) == 0


@pytest.mark.django_db
class TestUpdate:
    def test_update_video(self):
        repository = DjangoORMVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Test Video",
            description="A test video",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository.save(video)

        video.title = "Updated Test Video"
        video.description = "An updated test video"
        repository.update(video)

        updated_video = repository.get_by_id(id=video.id)
        assert updated_video.title == "Updated Test Video"
        assert updated_video.description == "An updated test video"

    def test_update_non_existent_video(self):
        repository = DjangoORMVideoRepository()
        video = Video(
            id=uuid.uuid4(),
            title="Non-existent Video",
            description="This video does not exist",
            launch_year=2023,
            opened=True,
            duration=120,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        
        repository.update(video)
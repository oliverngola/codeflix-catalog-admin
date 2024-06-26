import uuid
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository

@pytest.fixture
def category_movie():
    return  Category(
        name="Movie",
        description="Movie description",
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = '/api/categories/'
        response = APIClient().get(url)

        expected_data = {
            "data": [
                 {
                    "id": str(category_documentary.id),
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True
                },
                {
                    "id": str(category_movie.id),
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": 2, 
                "total": 2
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = f'/api/categories/1234567/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exits(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().get(url)

        expected_data = {
            "data":  {
                "id": str(category_documentary.id),
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_when_category_does_exist_return_404(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_return_400(self) -> None:
        url = f'/api/categories/'
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Documentary description"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = f'/api/categories/'
        response = APIClient().post(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = uuid.UUID(response.data["id"])
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Documentary",
            description="Documentary description"
        )

        assert category_repository.list() == [
            Category(
                id=uuid.UUID(response.data["id"]),
                name="Documentary",
                description="Documentary description"
            )
        ]

    
@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_return_400(self) -> None:
        url = f'/api/categories/12345677/'
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "Documentary description"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."]
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_documentary)

        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().put(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
                "is_active": False
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        update_category = category_repository.get_by_id(category_documentary.id)

        assert update_category.name == "Movie"
        assert update_category.description == "Movie description"
        assert update_category.is_active is False

    def test_when_category_does_not_exist(self) -> None:
        url = f'/api/categories/{uuid.uuid4()}/'

        response = APIClient().put(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
                "is_active": False
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_category_does_not_exist(self) -> None:
        url = f'/api/categories/{uuid.uuid4()}/'

        response = APIClient().patch(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
                "is_active": False
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_payload_is_invalid_return_400(self) -> None:
        url = f'/api/categories/12345677/'
        response = APIClient().patch(
            url,
            data={
                "name": "",
                "description": "Documentary description"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."]
        }

    @pytest.mark.parametrize(
        "payload,expected_category_dict",
        [
            (
                {
                    "name": "Not Movie",
                },
                {
                    "name": "Not Movie",
                    "description": "Movie description",
                    "is_active": True,
                },
            ),
            (
                {
                    "description": "Another description",
                },
                {
                    "name": "Movie",
                    "description": "Another description",
                    "is_active": True,
                },
            ),
            (
                {
                    "is_active": False,
                },
                {
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": False,
                },
            ),
        ],
    )
    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        payload: dict,
        expected_category_dict: dict,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)

        url = f'/api/categories/{category_movie.id}/'
        response = APIClient().patch(url, data=payload)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == expected_category_dict["name"]
        assert updated_category.description == expected_category_dict["description"]
        assert updated_category.is_active == expected_category_dict["is_active"]


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid_return_400(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url = f'/api/categories/1234567/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exits(
        self,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_documentary)

        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category_documentary.id) is None
        assert category_repository.list() == []

    def test_when_category_does_exist_return_404(
        self,
        category_documentary: Category
    ) -> None:
        url = f'/api/categories/{category_documentary.id}/'
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

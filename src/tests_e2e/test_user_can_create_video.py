import pytest
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGINATION_SIZE


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateVideoWithoutMedia:
    def test_user_can_create_video_without_media(self, api_client: APIClient) -> None:
        # Access the video list and verify no videos exist
        list_response = api_client.get("/api/videos/")
        assert list_response.data == {
            "data": [],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGINATION_SIZE,
                "total": 0,
            }
        }

        # Create a category
        created_category = api_client.post(
            "/api/categories/",
            {
                "name": "Movie",
                "description": "Movie description",
            },
        )
        created_category_id = created_category.data["id"]
        assert created_category.status_code == 201

        # Create a video without media
        create_response = api_client.post(
            "/api/videos/",
            {
                "title": "title",
                "description": "description",
                "launch_year": 2019,
                "opened": True,
                "rating": "L",
                "duration": 1,
                "categories": [
                    created_category_id
                ],
                "genres": [],
                "cast_members": []
            },
        )
        assert create_response.status_code == 201
        created_video_id = create_response.data["id"]

        # # Verify the created video appears in the list
        assert api_client.get("/api/videos/").data == {
            "data": [
                {
                    "id": created_video_id,
                    "title": "title",
                    "description": "description",
                    "year_launched": 2019,
                    "opened": True,
                    "rating": "L",
                    "duration": 1,
                    "link": "",
                    "categories": [
                    "Movie"
                    ],
                    "genres": [],
                    "cast_members": [],
                    "banner_file_url": "",
                    "thumb_file_url": "",
                    "video_file_url": ""
                }
            ],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGINATION_SIZE,
                "total": 1
            }
        }

    def test_video_list_pagination(self, api_client: APIClient) -> None:
        # Create a category
        created_category = api_client.post(
            "/api/categories/",
            {
                "name": "Movie",
                "description": "Movie description",
            },
        )
        created_category_id = created_category.data["id"]
        assert created_category.status_code == 201

        # Create two videos
        video_ids = []
        for i in range(2):
            create_response = api_client.post(
                "/api/videos/",
                {
                    "title": f"title-{i}",
                    "description": f"description-{i}",
                    "launch_year": 2020 + i,
                    "opened": False,
                    "rating": "L",
                    "duration": 10 + i,
                    "categories": [created_category_id],
                    "genres": [],
                    "cast_members": []
                },
            )
            assert create_response.status_code == 201
            video_ids.append(create_response.data["id"])

        # List videos with per_page=1 to test pagination
        list_response = api_client.get("/api/videos/?per_page=1")
        assert list_response.status_code == 200
        assert list_response.data["meta"]["per_page"] == 2
        assert list_response.data["meta"]["total"] == 2
        assert len(list_response.data["data"]) == 2

    def test_create_video_invalid_payload(self, api_client: APIClient) -> None:
        # Try to create a video with missing required fields
        response = api_client.post("/api/videos/", {})
        assert response.status_code == 400
        assert "title" in response.data
        assert "description" in response.data
        assert "launch_year" in response.data

    def test_create_video_with_invalid_category(self, api_client: APIClient) -> None:
        # Try to create a video with a non-existent category
        response = api_client.post(
            "/api/videos/",
            {
                "title": "title",
                "description": "description",
                "launch_year": 2022,
                "opened": True,
                "rating": "L",
                "duration": 5,
                "categories": ["non-existent-category-id"],
                "genres": [],
                "cast_members": []
            },
        )
        assert response.status_code == 400
        assert "categories" in response.data
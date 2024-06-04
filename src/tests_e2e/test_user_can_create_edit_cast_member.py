import pytest
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGINATION_SIZE


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateAndEditCastMember:
    def test_user_can_create_and_edit_cast_member(self, api_client: APIClient) -> None:
        list_response = api_client.get("/api/cast_members/")
        assert list_response.data == {
            "data": [],
            "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGINATION_SIZE,
                "total": 0,
            }
        }

        # Cria um cast member
        create_response = api_client.post(
            "/api/cast_members/",
            {
                "name": "John Doe",
                "type": "DIRECTOR",
            },
        )
        assert create_response.status_code == 201
        created_cast_member_id = create_response.data["id"]

        # Verifica que cast member criada aparece na listagem
        assert api_client.get("/api/cast_members/").data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "John Doe",
                    "type": "DIRECTOR"
                }
            ],
             "meta": {
                "current_page": 1,
                "per_page": DEFAULT_PAGINATION_SIZE,
                "total": 1
            }
        }

        # Edita cast member criada
        edit_response = api_client.put(
            f"/api/cast_members/{created_cast_member_id}/",
            {
                "name": "William",
                "type": "ACTOR",
            },
        )
        assert edit_response.status_code == 204

        # Verifica que cast member editada aparece na listagem
        api_client.get("/api/cast_members/").data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "William",
                    "description": "ACTOR",
                }
            ]
        }

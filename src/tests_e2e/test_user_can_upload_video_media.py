import json, pytest, pika, threading
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from rest_framework.test import APIClient

from src.config import DEFAULT_PAGINATION_SIZE

def start_consumer():
    call_command('startconsumer')

def send_rabbitmq_message(message: dict) -> None:
    QUEUE = "videos.converted"
    HOST = "localhost"
    PORT = 5672

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=HOST,
            port=PORT,
        ),
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(message))

    print("Sent message")
    connection.close()

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUpdateVideoWithMedia:
    def test_user_can_create_video_with_media(self, api_client: APIClient) -> None:
        t = threading.Thread(target=start_consumer, daemon=True)
        t.start()

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

        # Create a genre
        created_genre = api_client.post(
            "/api/genres/",
            {
                "name": "Genre",
                "categories": [created_category_id],
            },
        )
        created_genre_id = created_genre.data["id"]
        assert created_genre.status_code == 201

        # Create a cast member
        created_cast_member = api_client.post(
            "/api/cast_members/",
            {
                "name": "JOHN DOE",
                "type": "DIRECTOR",
            },
        )
        created_cast_member_id = created_cast_member.data["id"]
        assert created_cast_member.status_code == 201

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
                "genres": [
                    created_genre_id
                ],
                "cast_members": [
                    created_cast_member_id
                ]
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
                        created_category_id
                    ],
                    "genres": [
                        created_genre_id
                    ],
                    "cast_members": [
                        created_cast_member_id
                    ],
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

        # Update the video with media files 
        mocked_video = SimpleUploadedFile(
            name='test.mp4',
            content=open(f"{settings.BASE_DIR}/test.mp4", 'rb').read(),
            content_type='video/mp4'
        )
        update_response = api_client.patch(
            f"/api/videos/{created_video_id}/",
            {
                "video_file": mocked_video,
            },   
            format='multipart'         
        )
        assert update_response.status_code == 200

        # Simulate the message from RabbitMQ indicating video conversion is done
        resource_id = f"{created_video_id}.VIDEO"   
        send_rabbitmq_message({
            "error": "",
            "video": {
                "resource_id": resource_id,
                "encoded_video_folder": f"/videos/{created_video_id}/test.mp4",
            },
            "status": "COMPLETED",
        })

        # Wait for the consumer to process the message
        t.join(timeout=10)

        # Verify the video now has the media file URL
        retrieve_response = api_client.get(f"/api/videos/{created_video_id}/")
        assert retrieve_response.status_code == 200
        assert retrieve_response.data["data"]["video_file_url"] == f"videos/{created_video_id}/test.mp4"
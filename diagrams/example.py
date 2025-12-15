# referencias/test_Desafio: Teste end-to-end para eventos.md

import os
import time
import uuid
import requests
import pytest

RABBITMQ_EXAMPLE = "../code_examples/send_message_to_rabbit_mq.py"
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def create_entity(endpoint, payload):
   resp = requests.post(f"{API_URL}/{endpoint}/", json=payload)
   resp.raise_for_status()
   return resp.json()["id"]

def upload_media(video_id, file_path):
   with open(file_path, "rb") as f:
      files = {"file": f}
      resp = requests.post(f"{API_URL}/videos/{video_id}/upload/", files=files)
      resp.raise_for_status()
      return resp.json()

def get_video(video_id):
   resp = requests.get(f"{API_URL}/videos/{video_id}/")
   resp.raise_for_status()
   return resp.json()

def send_rabbitmq_message(video_id):
   # Use the example script to send a message to RabbitMQ
   # Assumes the script takes video_id as an argument
   os.system(f"python {RABBITMQ_EXAMPLE} {video_id}")

@pytest.mark.end2end
def test_video_media_processing_end_to_end(tmp_path):
   # 1. Create Category, Genre, CastMember
   category_id = create_entity("categories", {"name": "Test Category"})
   genre_id = create_entity("genres", {"name": "Test Genre"})
   cast_member_id = create_entity("cast_members", {"name": "Test Cast"})

   # 2. Create Video
   video_payload = {
      "title": "Test Video",
      "description": "End-to-end test video",
      "categories": [category_id],
      "genres": [genre_id],
      "cast_members": [cast_member_id]
   }
   video_id = create_entity("videos", video_payload)

   # 3. Upload media
   # Create a dummy media file
   media_file = tmp_path / "test.mp4"
   media_file.write_bytes(b"dummy video content")
   upload_media(video_id, str(media_file))

   # 4. Publish event to RabbitMQ
   send_rabbitmq_message(video_id)

   # 5. Poll for processing completion
   timeout = 60  # seconds
   interval = 5
   for _ in range(timeout // interval):
      video = get_video(video_id)
      status = video.get("video", {}).get("status")
      if status == "COMPLETED":
         break
      time.sleep(interval)
   else:
      pytest.fail("Media was not processed to COMPLETED status in time")

   assert video["video"]["status"] == "COMPLETED"
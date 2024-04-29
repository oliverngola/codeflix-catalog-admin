from django.test import TestCase
from rest_framework.test import APITestCase

class TestCategoryAPI(APITestCase):
    def test_list_category(self):
        url = "/api/categories/"
        response = self.client.get(url)

        except_data = [
            {
                "id": "b5944983-7177-4a6e-a72a-26a9f330d20e",
                "name": "Movie",
                "description": "Movie Descriptin",  
                "is_active": True
            },
            {
                "id": "c06803a0-58a0-41bd-9094-b1f14a572e3f",
                "name": "Documentary",
                "description": "Documentary Descriptin",  
                "is_active": True
            }
        ]

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, except_data)


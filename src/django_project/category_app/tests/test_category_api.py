from rest_framework.test import APITestCase

from src.core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel


class TestCategoryAPI(APITestCase):
    def test_list_category(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria para séries",
        )
        repository = DjangoORMCategoryRepository(CategoryModel)
        repository.save(category_filme)
        repository.save(category_serie)
        url = "/api/categories/"
        response = self.client.get(url)

        except_data = [
            {
                "id": str(category_filme.id),
                "name": category_filme.name,
                "description": category_filme.description,  
                "is_active": category_filme.is_active
            },
            {
                "id": str(category_serie.id),
                "name": category_serie.name,
                "description": category_serie.description,  
                "is_active": category_serie.is_active
            }
        ]

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, except_data)


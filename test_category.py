import unittest, uuid
from uuid import UUID

from category import Category

class TestCategory(unittest.TestCase):
    def test_name_is_requerid(self):
        with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with self.assertRaisesRegex(TypeError, "name must have less than 256 characters"):
            Category("a"*256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="Filme")
        self.assertEqual(type(category.id), UUID)

    def test_created_category_with_default_values(self):
        category = Category("Filme")
        self.assertEqual(category.name, "Filme")
        self.assertEqual(category.description, "")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_as_active_by_default(self):
        category = Category("Filme")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filme",
            description="Filmes em Geral",
            is_active=False
        )
        self.assertEqual(category.id, cat_id)
        self.assertEqual(category.name, "Filme")
        self.assertEqual(category.description, "Filmes em Geral")
        self.assertEqual(category.is_active, False)

    def test_category_str(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name = "Filme",
            description = "Filmes em geral",
            is_active=False
        )
        self.assertEqual(str(category), "Filme - Filmes em geral False")

    def test_category_repr(self):
        cat_id = uuid.uuid4()
        name = "Filme"
        category = Category(
            id=cat_id,
            name = name,
            description = "Filmes em geral",
            is_active=False
        )
        self.assertEqual(repr(category), f"<Category {name} ({cat_id})>")
    
if __name__ == "__main__":
    unittest.main()

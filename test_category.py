import uuid, pytest
from uuid import UUID

from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="Filme")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category("Filme")
        assert category.name == "Filme"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category("Filme")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filme",
            description="Filmes em Geral",
            is_active=False
        )
        assert category.id == cat_id
        assert category.name == "Filme"
        assert category.description == "Filmes em Geral"
        assert category.is_active is False

    def test_category_str(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name = "Filme",
            description = "Filmes em geral",
            is_active=False
        )
        assert str(category) == "Filme - Filmes em geral False"

    def test_category_repr(self):
        cat_id = uuid.uuid4()
        name = "Filme"
        category = Category(
            id=cat_id,
            name = name,
            description = "Filmes em geral",
            is_active=False
        )
        assert repr(category) == f"<Category {name} ({cat_id})>"

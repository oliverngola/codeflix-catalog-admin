import uuid, pytest
from uuid import UUID

from src.core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
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
    
    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme",description="Filmes em Geral")

        assert category.name == "Filme"
        assert category.description == "Filmes em Geral"

        category.update_category(name="Filmes de Acção", description="Filmes muito movimentados")
        
        assert category.name == "Filmes de Acção"
        assert category.description == "Filmes muito movimentados"

    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="Filme",description="Filmes em Geral")

        assert category.name == "Filme"
        assert category.description == "Filmes em Geral"

        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            category.update_category(name="a" * 256, description="Filmes muito fixe")

    def test_update_category_with_empty_name(self):
        category = Category(name="Filme",description="Filmes em Geral")

        assert category.name == "Filme"
        assert category.description == "Filmes em Geral"

        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update_category(name="", description="Filmes muito fixe")

class TestActivateCategory:
    def test_activate_inactive_category(self):
        category = Category(
            name="Filme",
            description="Filmes em Geral", 
            is_active=False
        )
        
        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(
            name="Filme",
            description="Filmes em Geral", 
            is_active=True
        )
        
        category.activate()

        assert category.is_active is True

class TestDeactivateCategory:
    def test_deactivate_active_category(self):
        category = Category(
            name="Filme",
            description="Filmes em Geral", 
            is_active=True
        )
        
        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        category = Category(
            name="Filme",
            description="Filmes em Geral", 
            is_active=False
        )
        
        category.deactivate()

        assert category.is_active is False

class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(name="Filmes", id=common_id)
        category_2 = Category(name="Filmes", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass
        
        common_id = uuid.uuid4()
        category_1 = Category(name="Filmes", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category_1 != dummy

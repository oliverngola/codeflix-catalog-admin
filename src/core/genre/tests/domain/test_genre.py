import uuid, pytest
from uuid import UUID

from src.core.genre.domain.genre import Genre

class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Genre(name="a" * 256)

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")

    def test_create_genre_with_default_value(self):
        genre = Genre(name="Romance")
        assert isinstance(genre.id, UUID)
        assert genre.name == "Romance"
        assert genre.is_active is True
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        categories = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre(
            id=cat_id,
            name="Romance",
            is_active=False,
            categories=categories
        )
        assert genre.id == cat_id
        assert genre.name == "Romance"
        assert genre.is_active is False
        assert genre.categories == categories

    def test_genre_str(self):
        cat_id = uuid.uuid4()
        genre = Genre(
            id=cat_id,
            name = "Romance",
            is_active=False
        )
        assert str(genre) == "Romance - False"

    def test_genre_repr(self):
        cat_id = uuid.uuid4()
        name = "Romance"
        genre = Genre(
            id=cat_id,
            name = name,
            is_active=False
        )
        assert repr(genre) == f"<Genre {name} ({cat_id})>"
    
    
class TestChangeName:
    def test_change_genere_name(self):
        genre = Genre(name="Romance")

        assert genre.name == "Romance"

        genre.change_name(name="Action")
        
        assert genre.name == "Action"

    def test_update_genre_with_invalid_name_raises_exception(self):
        genre = Genre(name="Action")

        assert genre.name == "Action"

        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            genre.change_name(name="a" * 256)

    def test_update_genre_with_empty_name(self):
        genre = Genre(name="Romance")

        assert genre.name == "Romance"

        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.change_name(name="")


class TestAddCategory:
    def test_add_category_to_genre(self):
        genre = Genre(name="Terror")
        category_id = uuid.uuid4()

        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories


class TestRemoveCategory:
    def test_remove_category_from_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name="Terror", categories={category_id})

        assert category_id in genre.categories
        genre.remove_category(category_id)
        assert category_id not in genre.categories


class TestActivateGenre:
    def test_activate_inactive_genre(self):
        genre = Genre(
            name="Romance",
            is_active=False
        )
        
        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre(
            name="Romance",
            is_active=True
        )
        
        genre.activate()

        assert genre.is_active is True


class TestDeactivateGenre:
    def test_deactivate_active_genre(self):
        genre = Genre(
            name="Romance",
            is_active=True
        )
        
        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        genre = Genre(
            name="Romance",
            is_active=False
        )
        
        genre.deactivate()

        assert genre.is_active is False


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre_1 = Genre(name="Romance", id=common_id)
        genre_2 = Genre(name="Romance", id=common_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass
        
        common_id = uuid.uuid4()
        genre_1 = Genre(name="Romance", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert genre_1 != dummy

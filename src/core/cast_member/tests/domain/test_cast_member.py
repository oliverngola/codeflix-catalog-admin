import uuid, pytest
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 2 required positional arguments: 'name' and 'type'"):
            CastMember()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            CastMember(name="a" * 256, type=CastMemberType.ACTOR)

    def test_cast_member_must_be_created_with_id_as_uuid(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        assert isinstance(cast_member.id, UUID)

    def test_created_cast_member_with_default_values(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"

    def test_cast_member_is_created_with_provided_values(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        assert cast_member.id == cast_member_id
        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"

    def test_cast_member_str(self):
        cast_member_id = uuid.uuid4()
        cast_member = CastMember(
            id=cast_member_id,
            name = "John Doe",
            type=CastMemberType.ACTOR
        )
        assert str(cast_member) == "John Doe - ACTOR"

    def test_cast_member_repr(self):
        cast_member_id = uuid.uuid4()
        name = "John Doe"
        cast_member = CastMember(
            id=cast_member_id,
            name = "John Doe",
            type=CastMemberType.ACTOR
        )
        assert repr(cast_member) == f"<CastMember {name} ({cast_member_id})>"
    
    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

class TestUpdateCastMember:
    def test_update_cast_member_with_name_and_type(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"

        cast_member.update_cast_member(name="John John", type=CastMemberType.DIRECTOR)
        
        assert cast_member.name == "John John"
        assert cast_member.type == "DIRECTOR"

    def test_update_cast_member_with_invalid_name_raises_exception(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"

        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            cast_member.update_cast_member(name="a" * 256, type=CastMemberType.ACTOR)

    def test_update_cast_member_with_empty_name(self):
        cast_member = CastMember(name="John Doe",type=CastMemberType.ACTOR)

        assert cast_member.name == "John Doe"
        assert cast_member.type == "ACTOR"

        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member.update_cast_member(name="", type=CastMemberType.ACTOR)

class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        cast_member_1 = CastMember(name="John Doe", id=common_id, type=CastMemberType.ACTOR)
        cast_member_2 = CastMember(name="John Doe", id=common_id, type=CastMemberType.DIRECTOR)

        assert cast_member_1 == cast_member_2

    def test_equality_different_classes(self):
        class Dummy:
            pass
        
        common_id = uuid.uuid4()
        cast_member_1 = CastMember(name="John Doe", id=common_id, type=CastMemberType.ACTOR)
        dummy = Dummy()
        dummy.id = common_id

        assert cast_member_1 != dummy

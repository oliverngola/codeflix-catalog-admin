import uuid
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestSave:
    def test_can_save_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        repository.save(cast_member)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == cast_member


class TestGetById:
    def test_can_get_cast_member_by_id(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_willian = CastMember(
            name="Willian",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                cast_member_john,
                cast_member_willian,
            ]
        )

        cast_member = repository.get_by_id(cast_member_john.id)

        assert cast_member == cast_member_john

    def test_when_cast_member_does_not_exists_should_return_none(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                cast_member_john,
            ]
        )

        cast_member = repository.get_by_id(uuid.uuid4())

        assert cast_member is None


class TestDelete:
    def test_delete_cast_member(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_willian = CastMember(
            name="Willian",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                cast_member_john,
                cast_member_willian,
            ]
        )

        repository.delete(cast_member_john.id)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0] == cast_member_willian


class TestList:
    def test_list_cast_members(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_willian = CastMember(
            name="Willian",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                cast_member_john,
                cast_member_willian,
            ]
        )

        cast_member = repository.list()

        assert len(cast_member) == 2

    def test_list_empty_cast_members(self):
        repository = InMemoryCastMemberRepository(
            cast_members=[]
        )

        cast_member = repository.list()

        assert len(cast_member) == 0



class TestUpdate:
    def test_update_cast_member(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_willian = CastMember(
            name="Willian",
            type=CastMemberType.DIRECTOR,
        )
        repository = InMemoryCastMemberRepository(
            cast_members=[
                cast_member_john,
                cast_member_willian,
            ]
        )

        cast_member_john.name = "John Marketer"
        cast_member_john.type = CastMemberType.DIRECTOR
        repository.update(cast_member_john)

        assert len(repository.cast_members) == 2
        updated_cast_member = repository.get_by_id(cast_member_john.id)
        assert updated_cast_member.name == "John Marketer"
        assert updated_cast_member.type == "DIRECTOR"

    def test_update_non_existent_cast_member_does_not_raise_exception(self):
        repository = InMemoryCastMemberRepository(cast_members=[])

        cast_member = CastMember(
            name="John",
            type=CastMemberType.DIRECTOR,
        )
        repository.update(cast_member)

        assert len(repository.cast_members) == 0

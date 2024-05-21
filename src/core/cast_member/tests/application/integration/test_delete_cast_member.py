import uuid, pytest

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.delete_cast_member  import DeleteCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        cast_member_willian = CastMember(
            name="Willian Doe",
            type=CastMemberType.DIRECTOR
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member_john, cast_member_willian])

        use_case = DeleteCastMember(repository=repository)
        input = DeleteCastMember.Input(id=cast_member_john.id)
        
        assert repository.get_by_id(cast_member_john.id) is not None
        output = use_case.execute(input)
               
        assert repository.get_by_id(cast_member_john.id) is None
        assert output is None
        assert len(repository.cast_members) == 1


    def test_when_cast_member_does_not_exit_then_raise_exception(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        cast_member_willian = CastMember(
            name="Willian Doe",
            type=CastMemberType.DIRECTOR
        )

        repository = InMemoryCastMemberRepository(cast_members=[cast_member_john, cast_member_willian])
        use_case = DeleteCastMember(repository=repository)
        not_found_id = uuid.uuid4()
        input = DeleteCastMember.Input(id=not_found_id)

        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(input)


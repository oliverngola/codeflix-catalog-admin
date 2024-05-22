import uuid, pytest

from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.get_cast_member import GetCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestGetCastMember:
    def test_cast_member_get_by_id(self):
        cast_member_john = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        cast_member_willian = CastMember(
            name="Willian Doe",
            type=CastMemberType.DIRECTOR
        )

        repository = InMemoryCastMemberRepository(cast_members=[cast_member_john, cast_member_willian])
        use_case = GetCastMember(repository=repository)
        input = GetCastMember.Input(id=cast_member_john.id)
        
        response = use_case.execute(input)

        assert response == GetCastMember.Output(
            id=cast_member_john.id,
            name=cast_member_john.name,
            type=cast_member_john.type
        )

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
        use_case = GetCastMember(repository=repository)
        not_found_id = uuid.uuid4()
        input = GetCastMember.Input(id=not_found_id)

        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(input)

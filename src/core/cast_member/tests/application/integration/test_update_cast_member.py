from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestUpdateCastMember:
    def test_update_cast_member_with_provided_fields(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member=cast_member)
        use_case = UpdateCastMember(repository=repository)

        request = UpdateCastMember.Input(
            id=cast_member.id,
            name="Willian",
            type=CastMemberType.DIRECTOR
        )
        response = use_case.execute(request)

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert response is None
        assert updated_cast_member.name == "Willian"
        assert updated_cast_member.type == "DIRECTOR"
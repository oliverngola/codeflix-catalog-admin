from uuid import UUID
import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        input = CreateCastMember.Input(
            name="John Doe",
			type=CastMemberType.ACTOR
        )
        
        output = use_case.execute(input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert len(repository.cast_members) == 1
        
        persisted_cast_member = repository.cast_members[0]
        assert persisted_cast_member.id == output.id
        assert persisted_cast_member.name == "John Doe"
        assert persisted_cast_member.type == "ACTOR"

    def test_create_cast_member_with_invalid_data(self):
        with pytest.raises(InvalidCastMember, match="name cannot be empty") as exc_info:
            use_case = CreateCastMember(repository=InMemoryCastMemberRepository())
            use_case.execute(CreateCastMember.Input(name="", type=CastMemberType.ACTOR))

        assert exc_info.type is InvalidCastMember
        assert str(exc_info.value) == "name cannot be empty"

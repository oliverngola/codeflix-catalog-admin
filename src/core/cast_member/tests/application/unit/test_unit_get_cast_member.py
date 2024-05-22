from unittest.mock import create_autospec
import pytest, uuid

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.get_cast_member import GetCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUnitGetCastMember:
    def test_cast_member_get_by_id(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        mock_respository = create_autospec(CastMemberRepository)
        mock_respository.get_by_id.return_value = cast_member
        use_case = GetCastMember(repository=mock_respository)
        input = GetCastMember.Input(id=uuid.uuid4())
        
        response = use_case.execute(input)

        assert response == GetCastMember.Output(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type
        )

    def test_when_cast_member_not_found_then_raise_exception(self):
        mock_respository = create_autospec(CastMemberRepository)
        mock_respository.get_by_id.return_value = None
        use_case = GetCastMember(repository=mock_respository)
        input = GetCastMember.Input(id=uuid.uuid4())

        with pytest.raises(CastMemberNotFound):        
            response = use_case.execute(input)

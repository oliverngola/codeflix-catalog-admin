from unittest.mock import create_autospec

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUpdateCastMember:
    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )
        mock_respository = create_autospec(CastMemberRepository)
        mock_respository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=mock_respository)
        input = UpdateCastMember.Input(
            id=cast_member.id,
            name="Willian",
            type=CastMemberType.DIRECTOR
        )
        
        use_case.execute(input)

        assert cast_member.name == "Willian"
        assert cast_member.type == "DIRECTOR"
        mock_respository.update.assert_called_once_with(cast_member)


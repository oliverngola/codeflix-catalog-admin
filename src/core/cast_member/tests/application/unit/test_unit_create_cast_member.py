from unittest.mock import MagicMock
from uuid import UUID
import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember


class TestUnitCreateCastMember:
	def test_create_cast_member_with_valid_data(self):
		mock_repository = MagicMock(CastMemberRepository)
		use_case = CreateCastMember(repository=mock_repository)
		input = CreateCastMember.Input(
			name="John Doe",
			type=CastMemberType.ACTOR
		)
		
		response = use_case.execute(input)

		assert response.id is not None
		assert isinstance(response, CreateCastMember.Output)
		assert isinstance(response.id, UUID)
		assert mock_repository.save.called is True

	def test_create_cast_member_with_invalid_data(self):
		with pytest.raises(InvalidCastMember, match="name cannot be empty") as exc_info:
			use_case = CreateCastMember(repository=MagicMock(CastMemberRepository))
			use_case.execute(CreateCastMember.Input(name="", type=CastMemberType.ACTOR))

		assert exc_info.type is InvalidCastMember
		assert str(exc_info.value) == "name cannot be empty"

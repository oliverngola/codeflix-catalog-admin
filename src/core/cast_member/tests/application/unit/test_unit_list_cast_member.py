from unittest.mock import create_autospec

import pytest
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestListCastMember:
    @pytest.fixture
    def cast_member_john(self) -> CastMember:
        return CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR
        )

    @pytest.fixture
    def cast_member_willian(self) -> CastMember:
        return CastMember(
            name="Willian",
            type=CastMemberType.ACTOR
        )

    @pytest.fixture
    def mock_empty_repository(self) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        cast_member_john: CastMember,
        cast_member_willian: CastMember,
    ) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [
            cast_member_john,
            cast_member_willian,
        ]
        return repository

    def test_when_no_cast_members_then_return_empty_list(
        self,
        mock_empty_repository: CastMemberRepository,
    ) -> None:
        use_case = ListCastMember(repository=mock_empty_repository)
        output = use_case.execute(request=ListCastMember.Input())

        assert output == ListCastMember.Output(data=[])

    def test_when_cast_members_exist_then_return_mapped_list(
        self,
        mock_populated_repository: CastMemberRepository,
        cast_member_john: CastMember,
        cast_member_willian: CastMember,
    ) -> None:
        use_case = ListCastMember(repository=mock_populated_repository)
        output = use_case.execute(request=ListCastMember.Input())

        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=cast_member_john.id,
                    name=cast_member_john.name,
                    type=cast_member_john.type
                ),
                CastMemberOutput(
                    id=cast_member_willian.id,
                    name=cast_member_willian.name,
                    type=cast_member_willian.type
                ),
            ]
        )
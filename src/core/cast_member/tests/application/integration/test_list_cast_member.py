import pytest
from src.core._shared.application.list import ListOutputMeta
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


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
            type=CastMemberType.DIRECTOR
        )

    def test_when_no_categories_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=empty_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert output == ListCastMember.Output(data=[])

    def test_when_categories_exist_then_return_mapped_list(
        self,
        cast_member_john: CastMember,
        cast_member_willian: CastMember,
    ) -> None:
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member=cast_member_john)
        repository.save(cast_member=cast_member_willian)

        use_case = ListCastMember(repository=repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=cast_member_john.id,
                    name=cast_member_john.name,
                    type=CastMemberType.ACTOR,
                ),
                CastMemberOutput(
                    id=cast_member_willian.id,
                    name=cast_member_willian.name,
                    type=CastMemberType.DIRECTOR,
                ),
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2,
            ),
        )
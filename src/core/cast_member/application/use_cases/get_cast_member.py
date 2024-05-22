from dataclasses import dataclass
from uuid import UUID
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class GetCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> Output:
        cast_member = self.repository.get_by_id(id=input.id)
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with {input.id} not found")
        return self.Output(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )
from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> None:
        cast_member = self.repository.get_by_id(id=input.id)
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with {input.id} not found")

        try:
            cast_member.update_cast_member(name=input.name, type=input.type)
        except ValueError as error:
            raise InvalidCastMember(error)

        self.repository.update(cast_member)
from uuid import UUID
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, model: CastMemberORM | None = None):
        self.model = model or CastMemberORM

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_model = self.model.objects.get(id=id)
            return  CastMemberModelMapper.to_entity(cast_member_model)
        except self.model.DoesNotExist:
            return None
        
    def save(self, cast_member: CastMember) -> None:
        cast_member_orm = CastMemberModelMapper.to_model(cast_member)
        cast_member_orm.save()

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(cast_member_model)
            for cast_member_model in self.model.objects.all()
        ]

    def update(self, cast_member: CastMember) -> None:
        self.model.objects.filter(pk=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type,
        )


class CastMemberModelMapper:
    @staticmethod
    def to_entity(model: CastMemberORM) -> CastMember:
        return CastMember(
            id=model.id,
            name=model.name,
            type=CastMemberType(model.type)
        )

    @staticmethod
    def to_model(entity: CastMember) -> CastMemberORM:
        return CastMemberORM(
            id=entity.id,
            name=entity.name,
            type=entity.type,
        )
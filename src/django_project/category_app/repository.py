from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryORM


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, model: CategoryORM | None = None) -> None:
        self.model = model or CategoryORM

    def get_by_id(self, id) -> Category | None:
        try:
            category_model = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)
        except self.model.DoesNotExist:
            return None

    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
    
    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()
    
    def list(self) -> list[Category]:
        return [
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.model.objects.all()
        ]
    
    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

class CategoryModelMapper:
    @staticmethod
    def to_entity(model: CategoryORM) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(entity: Category) -> CategoryORM:
        return CategoryORM(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
        )
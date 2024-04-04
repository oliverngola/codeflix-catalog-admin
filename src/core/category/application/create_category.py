from uuid import UUID

from src.core.category.domain.category import Category

class InvalidCategoryData(Exception):
    pass


def create_category(name: str, description: str = "", is_active: bool = True) -> UUID:
    try:
        category = Category(name, description, is_active)
    except ValueError as err:
        raise InvalidCategoryData(err)
    return category.id
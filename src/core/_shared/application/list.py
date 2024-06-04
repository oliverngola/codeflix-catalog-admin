from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")

from src import config

@dataclass
class ListInput(Generic[T], ABC):
    order_by: str = T
    current_page: int = 1

@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total: int = 0


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
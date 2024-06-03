from dataclasses import dataclass, field
from typing import Set
from uuid import UUID, uuid4

from src.core._shared.notification import Notification

@dataclass
class Genre:
    name: str
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid4)

    notification: Notification = field(default_factory=Notification)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("name cannot be longer than 255")
        
        if not self.name:
            self.notification.add_error("name cannot be empty")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def __str__(self):
        return f"{self.name} - {self.is_active}" 
    
    def __repr__(self):
        return f"<Genre {self.name} ({self.id})>"
    
    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.id == other.id
    
    def change_name(self, name):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
        self.validate()

    def update_categories(self, category_ids: Set[UUID]) -> None:
        self.categories = category_ids
        self.validate()
        
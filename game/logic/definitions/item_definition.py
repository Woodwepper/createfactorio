from dataclasses import dataclass
from typing import Optional

from game.logic.enums.item_category import ItemCategory

@dataclass
class ItemDefinition:
    id: str
    name: str
    max_stack_size: int = 64
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    category: ItemCategory = ItemCategory.MATERIAL

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "stack_size": self.max_stack_size,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "category": self.category.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ItemDefinition":
        return cls(
            id=data["id"],
            name=data["name"],
            max_stack_size=data.get("stack_size", 64),
            entity_type=data.get("entity_type"),
            entity_id=data.get("entity_id"),
            category=ItemCategory(data.get("category", "material")),
        )

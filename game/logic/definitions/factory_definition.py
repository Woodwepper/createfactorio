from dataclasses import dataclass

@dataclass
class FactoryLevel:
    required_items: dict[str, int]
    module_slots: int

    def to_dict(self) -> dict:
        return {
            "required_items": self.required_items,
            "module_slots": self.module_slots,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FactoryLevel":
        return cls(
            required_items=data["required_items"],
            module_slots=data["module_slots"],
        )


@dataclass
class FactoryDefinition:
    id: str
    name: str
    levels: list[FactoryLevel]
    default_level: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "levels": [level.to_dict() for level in self.levels],
            "default_level": self.default_level,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FactoryDefinition":
        return cls(
            id=data["id"],
            name=data["name"],
            levels=[FactoryLevel.from_dict(level) for level in data["levels"]],
            default_level=data["default_level"],
        )

from dataclasses import dataclass

@dataclass
class ModuleLevel:
    level: int
    machine_slots: int

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "machine_slots": self.machine_slots,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModuleLevel":
        return cls(
            level=data["level"],
            machine_slots=data["machine_slots"],
        )


@dataclass
class ModuleDefinition:
    id: str
    name: str
    levels: list[ModuleLevel]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "levels": [level.to_dict() for level in self.levels],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModuleDefinition":
        return cls(
            id=data["id"],
            name=data["name"],
            levels=[ModuleLevel.from_dict(level) for level in data.get("levels", [])],
        )

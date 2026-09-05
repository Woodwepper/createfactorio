from dataclasses import dataclass

@dataclass(frozen=True)
class MachineDefinition:
    id: str
    name: str
    su_required: int
    cycles_per_craft: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "su_required": self.su_required,
            "cycles_per_craft": self.cycles_per_craft,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MachineDefinition":
        return cls(
            id=data["id"],
            name=data["name"],
            su_required=data["su_required"],
            cycles_per_craft=data.get("cycles_per_craft", 1),
        )

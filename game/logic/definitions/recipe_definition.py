from dataclasses import dataclass

from game.logic.definitions.resource_requirement import ResourceRequirement

@dataclass
class RecipeDefinition:
    name: str
    id: str

    craft_time: int

    required_machine: str
    inputs: list[ResourceRequirement]
    outputs: list[ResourceRequirement]

    manual_crafting: bool

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "craft_time": self.craft_time,
            "required_machine": self.required_machine,
            "inputs": [req.to_dict() for req in self.inputs],
            "outputs": [req.to_dict() for req in self.outputs],
            "manual_crafting": self.manual_crafting,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RecipeDefinition":
        return cls(
            id=data["id"],
            name=data["name"],
            craft_time=data["craft_time"],
            required_machine=data["required_machine"],
            inputs=[ResourceRequirement.from_dict(req) for req in data.get("inputs", [])],
            outputs=[ResourceRequirement.from_dict(req) for req in data.get("outputs", [])],
            manual_crafting=data.get("manual_crafting", False),
        )

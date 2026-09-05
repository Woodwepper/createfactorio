from dataclasses import dataclass
from typing import Optional

from game.logic.models.machine_instance import MachineInstance
from game.logic.definitions.module_definition import ModuleDefinition
from game.logic.enums.module_state import ModuleState
from game.logic.definitions.recipe_definition import RecipeDefinition


import uuid

@dataclass
class ModuleInstance:

    definition: ModuleDefinition

    machines: list[MachineInstance]

    assigned_recipe: Optional[RecipeDefinition]

    state: ModuleState
    current_level: int

    @property
    def uuid(self) -> str:
        return str(uuid.uuid4())

    @property
    def definition_id(self) -> str:
        return self.definition.id

    @property
    def max_machines(self) -> int:
        return self.definition.levels[self.current_level - 1].machine_slots

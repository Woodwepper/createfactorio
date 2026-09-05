from dataclasses import dataclass, field

import uuid

from game.logic.enums.factory_state import FactoryState
from game.logic.definitions.factory_definition import FactoryDefinition
from game.logic.models.module_instance import ModuleInstance
from game.logic.models.inventory_instance import InventoryInstance

@dataclass
class FactoryBuilding:
    name: str
    definition: FactoryDefinition
    cell: tuple[int, int]
    level: int = 1
    icon: str = "default/factory.png"
    modules: list[ModuleInstance] = field(default_factory=list)
    inventory: InventoryInstance = field(default_factory=InventoryInstance)
    status: FactoryState = FactoryState.IDLE

    @property
    def uuid(self):
        return str(uuid.uuid4())

    @property
    def definition_id(self):
        return self.definition.id

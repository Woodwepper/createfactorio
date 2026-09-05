from dataclasses import dataclass
import uuid

from game.logic.definitions.machine_definition import MachineDefinition

@dataclass
class MachineInstance:

    definition: MachineDefinition

    @property
    def uuid(self) -> str:
        return str(uuid.uuid4())

    @property
    def definition_id(self) -> str:
        return self.definition.id

from dataclasses import dataclass, field

from game.logic.definitions.factory_definition import FactoryDefinition
from game.logic.definitions.item_definition import ItemDefinition
from game.logic.definitions.machine_definition import MachineDefinition
from game.logic.definitions.module_definition import ModuleDefinition
from game.logic.definitions.recipe_definition import RecipeDefinition
from game.logic.enums.construction_type import ConstructionType
from game.logic.content.registry import Registry


@dataclass(frozen=True)
class ConstructionOption:
    construction_type: ConstructionType
    definition_id: str
    label: str


@dataclass
class GameDefinitions:
    """Central catalog of all definitions available to a World."""

    items: Registry[ItemDefinition] = field(default_factory=Registry)
    machines: Registry[MachineDefinition] = field(default_factory=Registry)
    recipes: Registry[RecipeDefinition] = field(default_factory=Registry)
    modules: Registry[ModuleDefinition] = field(default_factory=Registry)
    factories: Registry[FactoryDefinition] = field(default_factory=Registry)

    def get_construction_definition(
        self,
        construction_type: ConstructionType,
        definition_id: str,
    ) -> object | None:
        registry = self._construction_registry(construction_type)
        if registry is None:
            return None
        return registry.get(definition_id)

    def get_construction_options(self) -> list[ConstructionOption]:
        options: list[ConstructionOption] = []

        for definition in self.factories.get_all().values():
            options.append(
                ConstructionOption(
                    construction_type=ConstructionType.FACTORY,
                    definition_id=definition.id,
                    label=definition.name,
                )
            )

        return options

    def _construction_registry(
        self,
        construction_type: ConstructionType,
    ) -> Registry | None:
        registries = {
            ConstructionType.FACTORY: self.factories,
            ConstructionType.MODULE: self.modules,
        }
        return registries.get(construction_type)

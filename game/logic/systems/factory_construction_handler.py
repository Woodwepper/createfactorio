from game.logic.definitions.factory_definition import FactoryDefinition
from game.logic.models.factory_building import FactoryBuilding


class FactoryConstructionHandler:
    """Factory-specific construction rules."""

    @staticmethod
    def required_items(definition: FactoryDefinition) -> dict[str, int]:
        level_index = definition.default_level - 1
        return definition.levels[level_index].required_items

    @staticmethod
    def create_instance(
        definition: FactoryDefinition,
        cell: tuple[int, int],
    ) -> FactoryBuilding:
        return FactoryBuilding(
            name=definition.name,
            definition=definition,
            cell=cell,
            level=definition.default_level,
        )

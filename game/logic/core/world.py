from dataclasses import dataclass, field

from game.logic.content.game_definitions import GameDefinitions
from game.logic.models.construction_instance import ConstructionInstance
from game.logic.models.inventory_instance import InventoryInstance


@dataclass
class World:
    definitions: GameDefinitions
    tick_count: int = 0
    player_inventory: InventoryInstance = field(default_factory=InventoryInstance)
    buildings: dict[tuple[int, int], ConstructionInstance] = field(default_factory=dict)

    def update(self) -> None:
        self.tick_count += 1

    def get_tick_count(self) -> int:
        return self.tick_count

    def get_building_at(
        self,
        cell: tuple[int, int],
    ) -> ConstructionInstance | None:
        return self.buildings.get(cell)

    def add_building(self, building: ConstructionInstance) -> None:
        if self.get_building_at(building.cell) is not None:
            raise RuntimeError(f"Cell is already occupied: {building.cell}")

        self.buildings[building.cell] = building

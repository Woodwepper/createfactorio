from dataclasses import dataclass, field

from game.logic.systems.order_system import OrderSystem
from .world import World


@dataclass
class Simulation:
    world: World
    order_system: OrderSystem = field(default_factory=OrderSystem)
    is_running: bool = False

    def tick(self) -> None:
        if not self.is_running:
            return

        self.order_system.process_pending(self.world)
        self.world.update()

from collections import deque
from dataclasses import dataclass, field

from game.logic.core.world import World
from game.logic.orders.order_result import OrderResult
from game.logic.orders.place_construction_order import PlaceConstructionOrder
from game.logic.systems.construction_system import ConstructionSystem


@dataclass
class OrderSystem:
    construction_system: ConstructionSystem = field(
        default_factory=ConstructionSystem.with_default_handlers
    )
    pending_orders: deque[PlaceConstructionOrder] = field(default_factory=deque)
    last_results: list[OrderResult] = field(default_factory=list)

    def enqueue(self, order: PlaceConstructionOrder) -> None:
        self.pending_orders.append(order)

    def process_pending(self, world: World) -> list[OrderResult]:
        self.last_results.clear()

        while self.pending_orders:
            order = self.pending_orders.popleft()
            result = self.construction_system.process(order, world)
            self.last_results.append(result)
            print(result.message)

        return list(self.last_results)

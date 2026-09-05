from dataclasses import dataclass
from typing import Callable

from game.logic.core.world import World
from game.logic.enums.construction_type import ConstructionType
from game.logic.models.construction_instance import ConstructionInstance
from game.logic.orders.order_result import OrderResult
from game.logic.orders.place_construction_order import PlaceConstructionOrder
from game.logic.systems.factory_construction_handler import FactoryConstructionHandler


@dataclass(frozen=True)
class ConstructionHandler:
    required_items: Callable[[object], dict[str, int]]
    create_instance: Callable[
        [object, tuple[int, int]],
        ConstructionInstance,
    ]


class ConstructionSystem:
    """Dispatches construction orders to registered construction handlers."""

    def __init__(self) -> None:
        self._handlers: dict[ConstructionType, ConstructionHandler] = {}

    @classmethod
    def with_default_handlers(cls) -> "ConstructionSystem":
        system = cls()
        system.register_handler(
            ConstructionType.FACTORY,
            ConstructionHandler(
                required_items=FactoryConstructionHandler.required_items,
                create_instance=FactoryConstructionHandler.create_instance,
            ),
        )
        return system

    def register_handler(
        self,
        construction_type: ConstructionType,
        handler: ConstructionHandler,
    ) -> None:
        self._handlers[construction_type] = handler

    def process(
        self,
        order: PlaceConstructionOrder,
        world: World,
    ) -> OrderResult:
        handler = self._handlers.get(order.construction_type)
        if handler is None:
            return OrderResult(
                order_id=order.order_id,
                success=False,
                message=(
                    "No construction handler registered for: "
                    f"{order.construction_type.value}"
                ),
            )

        definition = world.definitions.get_construction_definition(
            order.construction_type,
            order.definition_id,
        )
        if definition is None:
            return OrderResult(
                order_id=order.order_id,
                success=False,
                message=f"Construction definition not found: {order.definition_id}",
            )

        if world.get_building_at(order.cell) is not None:
            return OrderResult(
                order_id=order.order_id,
                success=False,
                message=f"Cell is already occupied: {order.cell}",
            )

        required_items = handler.required_items(definition)
        for item_id, amount in required_items.items():
            if world.player_inventory.item_registry.get(item_id) is None:
                return OrderResult(
                    order_id=order.order_id,
                    success=False,
                    message=f"Item definition not found: {item_id}",
                )

            if amount <= 0:
                return OrderResult(
                    order_id=order.order_id,
                    success=False,
                    message=f"Invalid required amount for item: {item_id}",
                )

            if not world.player_inventory.contains(item_id, amount):
                return OrderResult(
                    order_id=order.order_id,
                    success=False,
                    message=f"Not enough items: {item_id}",
                )

        for item_id, amount in required_items.items():
            world.player_inventory.consume(item_id, amount)

        instance = handler.create_instance(definition, order.cell)
        world.add_building(instance)

        return OrderResult(
            order_id=order.order_id,
            success=True,
            message=f"Construction created at {order.cell}",
        )

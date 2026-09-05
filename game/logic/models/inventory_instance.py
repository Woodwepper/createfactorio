from dataclasses import dataclass, field

from game.logic.content.registry import Registry
from game.logic.definitions.item_definition import ItemDefinition
from game.logic.models.item_stack_instance import ItemStackInstance


@dataclass
class InventoryInstance:
    """Slot-based inventory used by the player and game buildings."""

    slot_count: int = 27
    item_registry: Registry[ItemDefinition] = field(default_factory=Registry)
    slots: list[ItemStackInstance | None] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.slot_count < 0:
            raise ValueError("slot_count cannot be negative")

        if not self.slots:
            self.slots = [None] * self.slot_count
        elif len(self.slots) != self.slot_count:
            raise ValueError("slots length must match slot_count")

    def get_slot(self, index: int) -> ItemStackInstance | None:
        self._validate_index(index)
        return self.slots[index]

    def set_slot(self, index: int, stack: ItemStackInstance | None) -> None:
        self._validate_index(index)
        if stack is not None:
            self._validate_stack(stack)
        self.slots[index] = stack

    def get_quantity(self, item_id: str) -> int:
        return sum(
            stack.amount
            for stack in self.slots
            if stack is not None and stack.item_id == item_id
        )

    def contains(self, item_id: str, amount: int) -> bool:
        if amount < 0:
            raise ValueError("amount cannot be negative")
        return self.get_quantity(item_id) >= amount

    def can_add(self, stack: ItemStackInstance) -> bool:
        definition = self._get_definition(stack.item_id)
        remaining = stack.amount

        for current in self.slots:
            if current is not None and current.is_compatible_with(stack):
                remaining -= max(0, definition.max_stack_size - current.amount)
                if remaining <= 0:
                    return True

        for current in self.slots:
            if current is None:
                remaining -= definition.max_stack_size
                if remaining <= 0:
                    return True

        return False

    def add_stack(self, stack: ItemStackInstance) -> None:
        if stack.amount <= 0:
            raise ValueError("amount must be greater than zero")

        definition = self._get_definition(stack.item_id)

        if not self.can_add(stack):
            raise RuntimeError("Inventory has no space for this item stack")

        remaining = stack.amount

        for current in self.slots:
            if current is None or not current.is_compatible_with(stack):
                continue

            available = definition.max_stack_size - current.amount
            added = min(available, remaining)
            current.amount += added
            remaining -= added

            if remaining == 0:
                return

        for index, current in enumerate(self.slots):
            if current is not None:
                continue

            added = min(definition.max_stack_size, remaining)
            self.slots[index] = ItemStackInstance(
                item_id=stack.item_id,
                amount=added,
                data=stack.data,
            )
            remaining -= added

            if remaining == 0:
                return

    def consume(self, item_id: str, amount: int) -> None:
        if amount <= 0:
            raise ValueError("amount must be greater than zero")
        if not self.contains(item_id, amount):
            raise RuntimeError(f"Not enough items: {item_id}")

        remaining = amount
        for index, stack in enumerate(self.slots):
            if stack is None or stack.item_id != item_id:
                continue

            consumed = min(stack.amount, remaining)
            stack.amount -= consumed
            remaining -= consumed

            if stack.amount == 0:
                self.slots[index] = None

            if remaining == 0:
                return

    def copy(self) -> "InventoryInstance":
        return InventoryInstance(
            slot_count=self.slot_count,
            item_registry=self.item_registry,
            slots=[stack.copy() if stack is not None else None for stack in self.slots],
        )

    def _get_definition(self, item_id: str) -> ItemDefinition:
        definition = self.item_registry.get(item_id)
        if definition is None:
            raise RuntimeError(f"Item definition not found: {item_id}")
        return definition

    def _validate_stack(self, stack: ItemStackInstance) -> None:
        definition = self._get_definition(stack.item_id)
        if stack.amount > definition.max_stack_size:
            raise ValueError(
                f"A single stack cannot exceed {definition.max_stack_size} items"
            )

    def _validate_index(self, index: int) -> None:
        if not 0 <= index < self.slot_count:
            raise IndexError(f"Invalid inventory slot: {index}")

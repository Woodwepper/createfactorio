from game.logic.models.inventory_instance import InventoryInstance
from game.logic.models.item_stack_instance import ItemStackInstance
from game.logic.definitions.item_definition import ItemDefinition
from game.logic.content import Registry

registry = Registry()
iron_ingot = ItemDefinition(
    id="iron_ingot",
    name="Iron Ingot",
    max_stack_size=64,
)
registry.register(iron_ingot)

inventory_a = InventoryInstance(item_registry=registry)
inventory_b = InventoryInstance(item_registry=registry)

for i in range(27):
    inventory_a.set_slot(i, ItemStackInstance(item_id="iron_ingot", amount=1))
    inventory_b.set_slot(i, ItemStackInstance(item_id="iron_ingot", amount=1))

def combine_inventories(
    inv_a: InventoryInstance,
    inv_b: InventoryInstance,
) -> InventoryInstance:
    result = inv_a.copy()

    for stack in inv_b.slots:
        if stack is not None:
            result.add_stack(stack.copy())

    return result


def mostrar_inventario(
    inventory: InventoryInstance,
    columns: int = 3,
) -> None:
    """Muestra los slots y las cantidades de un inventario en consola."""
    if columns <= 0:
        raise ValueError("columns debe ser mayor que cero")

    slot_texts = []
    for index in range(inventory.slot_count):
        stack = inventory.get_slot(index)

        if stack is None:
            slot_texts.append(f"[{index:02}] Vacío")
            continue

        definition = inventory.item_registry.get(stack.item_id)
        item_name = definition.name if definition is not None else stack.item_id
        slot_texts.append(f"[{index:02}] {item_name} x{stack.amount}")

    cell_width = max(18, max((len(text) for text in slot_texts), default=18))
    border = "─" * (cell_width + 2)
    full_border = "┌" + "┬".join(border for _ in range(columns)) + "┐"
    middle_border = "├" + "┼".join(border for _ in range(columns)) + "┤"
    bottom_border = "└" + "┴".join(border for _ in range(columns)) + "┘"

    print("\\nInventario")
    print(full_border)

    for start in range(0, len(slot_texts), columns):
        row = slot_texts[start:start + columns]
        row += [""] * (columns - len(row))
        cells = [f" {text:<{cell_width}} " for text in row]
        print("│" + "│".join(cells) + "│")

        if start + columns < len(slot_texts):
            print(middle_border)

    print(bottom_border)
    total = sum(
        stack.amount
        for stack in inventory.slots
        if stack is not None
    )
    print(f"Total de objetos: {total}")

result = combine_inventories(inventory_a, inventory_b)
mostrar_inventario(result)
